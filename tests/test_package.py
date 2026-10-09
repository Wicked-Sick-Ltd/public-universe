"""Offline regression tests for generated examples and distributable contents."""

import importlib.util
import json
import os
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package", REPO / "scripts/package.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("plugin.json", json.dumps({
            "$schema": package.SCHEMA_ROOT + "plugin.schema.json", "name": "solar", "version": "0.2.0",
            "description": "Public astronomy", "repository": "https://example.org/solar", "license": "MIT",
            "extensions": {"com.openai": {"interface": {"displayName": "Solar"}}},
        }))
        self.write("mcp.json", json.dumps({
            "$schema": package.SCHEMA_ROOT + "mcp.schema.json",
            "mcpServers": {"solar-system-db": {"type": "streamable-http", "url": "https://example.org/mcp"}},
        }))
        for relative in ("README.md", "LICENSE", "NOTICE", "CHANGELOG.md", *package.DOCS):
            self.write(relative, "Public documentation\n")
        self.write("skills/example/SKILL.md", '---\nname: example\ndescription: >\n  Explain astronomy with public data.\nmetadata:\n  version: "0.1.0"\n---\nRead `references/data-caveats.md`.\n')
        self.write("skills/example/references/data-caveats.md", "Scientific caveats\n")
        package.generate(self.root)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def symlink(self, path, target, **kwargs):
        try:
            path.symlink_to(target, **kwargs)
        except OSError as error:
            if getattr(error, "winerror", None) == 1314:
                self.skipTest("Windows account lacks symlink privilege; exercised by Linux CI")
            raise

    def test_rejects_unknown_plugin_fields_before_generation(self):
        manifest = json.loads((self.root / "plugin.json").read_text())
        manifest["unsupportedField"] = True
        self.write("plugin.json", json.dumps(manifest))
        with self.assertRaisesRegex(package.ValidationError, "Unsupported plugin metadata: unsupportedField"):
            package.generate(self.root)

    def test_rejects_invalid_metadata_shapes(self):
        original = json.loads((self.root / "plugin.json").read_text())
        changes = (
            {"author": {"name": 42}}, {"author": {"name": True}},
            {"author": "Public Universe"}, {"author": {}},
            {"author": {"name": "Public Universe", "email": 42}},
            {"author": {"name": "Public Universe", "url": []}},
            {"author": {"name": "Public Universe", "unknown": "value"}},
            {"keywords": "astronomy"}, {"keywords": ["astronomy", 42]},
            {"keywords": [True]}, {"keywords": [""]},
            {"extensions": []}, {"extensions": {"com.openai": True}},
            {"homepage": False}, {"homepage": ""},
            {"description": 42}, {"repository": []}, {"license": True},
        )
        for change in changes:
            with self.subTest(change=change):
                self.write("plugin.json", json.dumps({**original, **change}))
                with self.assertRaises(package.ValidationError):
                    package.generate(self.root)

    def test_plugin_name_length_and_slug_are_checked(self):
        original = json.loads((self.root / "plugin.json").read_text())
        for name in ("a" * 65, "Solar", "solar--plugin", "../solar", True, 42):
            with self.subTest(name=name):
                self.write("plugin.json", json.dumps({**original, "name": name}))
                with self.assertRaisesRegex(package.ValidationError, "Plugin name"):
                    package.generate(self.root)
        self.write("plugin.json", json.dumps({**original, "name": "a" * 64}))
        package.generate(self.root)
        package.check(self.root)

    def test_rejects_unknown_mcp_fields(self):
        manifest = json.loads((self.root / "mcp.json").read_text())
        manifest["unsupportedField"] = True
        self.write("mcp.json", json.dumps(manifest))
        with self.assertRaisesRegex(package.ValidationError, "Unsupported MCP metadata: unsupportedField"):
            package.generate(self.root)

    def test_native_client_shapes_and_shared_endpoint(self):
        read = lambda path: json.loads((self.root / path).read_text())
        expected_url = "https://example.org/mcp"
        self.assertEqual(read(".mcp.json"), read("clients/claude.json"))
        self.assertEqual(read("clients/cursor.json")["mcpServers"]["solar-system-db"], {"url": expected_url})
        self.assertEqual(read("clients/vscode.json")["servers"]["solar-system-db"], {"type": "http", "url": expected_url})
        self.assertEqual(read("clients/copilot-cli.json")["mcpServers"]["solar-system-db"], {"type": "http", "url": expected_url, "tools": ["*"]})
        self.assertEqual(tomllib.loads((self.root / "clients/codex.toml").read_text())["mcp_servers"]["solar-system-db"]["url"], expected_url)
        self.assertNotIn("extensions", read(".claude-plugin/plugin.json"))
        self.assertNotIn("$schema", read(".claude-plugin/plugin.json"))
        gemini = read("gemini-extension.json")
        self.assertEqual(gemini["name"], read("plugin.json")["name"])
        self.assertEqual(gemini["version"], read("plugin.json")["version"])
        self.assertEqual(gemini["mcpServers"]["solar-system-db"], {"httpUrl": expected_url})
        marketplace = read("clients/openai-marketplace.json")
        self.assertEqual(marketplace["plugins"][0]["source"]["url"], "https://example.org/solar.git")

    def test_endpoint_change_requires_regeneration(self):
        path = self.root / "mcp.json"
        path.write_text(path.read_text().replace("example.org", "new.example.org"))
        with self.assertRaisesRegex(package.ValidationError, "Generated file drift"):
            package.check(self.root)
        package.generate(self.root)
        package.check(self.root)
        self.assertIn("new.example.org", (self.root / "clients/codex.toml").read_text())

    def test_manual_edit_detected(self):
        self.write("clients/vscode.json", "{}\n")
        with self.assertRaisesRegex(package.ValidationError, "Generated file drift: clients/vscode.json"):
            package.build(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_listing_icons_are_packaged_and_cannot_escape_root(self):
        manifest = json.loads((self.root / "plugin.json").read_text())
        interface = manifest["extensions"]["com.openai"]["interface"]
        interface.update(logo="./assets/icon.svg", composerIcon="./assets/icon.svg")
        self.write("plugin.json", json.dumps(manifest))
        self.write("assets/icon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"/>')
        package.generate(self.root)
        with zipfile.ZipFile(package.build(self.root)[0]) as archive:
            self.assertIn("assets/icon.svg", archive.namelist())
            self.assertIn("gemini-extension.json", archive.namelist())
        for invalid in ("../outside.svg", str(self.root / "assets/icon.svg")):
            with self.subTest(path=invalid):
                interface["logo"] = invalid
                self.write("plugin.json", json.dumps(manifest))
                package.generate(self.root)
                with self.assertRaises(package.ValidationError):
                    package.check(self.root)

    def test_archives_are_complete_deterministic_and_allowlisted(self):
        for relative in (".env", ".git/config", "notes.txt", "docs/private.md", "clients/secret.json", "skills/example/references/private.md"):
            self.write(relative, "SECRET DO NOT SHIP\n")
        first, legacy = package.build(self.root)
        initial = first.read_bytes()
        for path in self.root.rglob("*.md"):
            os.utime(path, (1750000000, 1750000000))
        package.build(self.root)
        self.assertEqual(initial, first.read_bytes())
        self.assertEqual(initial, legacy.read_bytes())
        self.assertNotIn(b"SECRET DO NOT SHIP", initial)
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(archive.namelist(), package.check(self.root))
            self.assertIn("skills/example/references/data-caveats.md", archive.namelist())
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertFalse(entry.filename.startswith("/"))
                self.assertNotIn("..", Path(entry.filename).parts)

    def test_every_repository_skill_and_reference_is_in_allowlist(self):
        files = set(package.skill_files(REPO))
        expected = {path.relative_to(REPO).as_posix() for path in (REPO / "skills").rglob("*.md")}
        self.assertEqual(files, expected)

    def test_missing_reference_is_error(self):
        (self.root / "skills/example/references/data-caveats.md").unlink()
        with self.assertRaisesRegex(package.ValidationError, "Missing package file"):
            package.check(self.root)

    def test_new_reference_requires_explicit_allowlist(self):
        path = self.root / "skills/example/SKILL.md"
        path.write_text(path.read_text() + "Read `references/new.md`.\n")
        self.write("skills/example/references/new.md", "New document")
        with self.assertRaisesRegex(package.ValidationError, "package allowlist"):
            package.check(self.root)

    def test_invalid_frontmatter_is_error(self):
        for content in ("No header", "---\nname: other\ndescription: Fine\n---\n", "---\nname: example\ndescription: >\n---\n"):
            with self.subTest(content=content):
                self.write("skills/example/SKILL.md", content)
                with self.assertRaises(package.ValidationError):
                    package.check(self.root)

    def test_windows_skill_line_endings(self):
        path = self.root / "skills/example/SKILL.md"
        path.write_bytes(path.read_text().replace("\n", "\r\n").encode())
        self.assertIn("skills/example/SKILL.md", package.check(self.root))

    def test_remote_configuration_rejects_credentials_and_non_https(self):
        for url in ("http://example.org/mcp", "https://user:pass@example.org/mcp", "https://example.org/mcp?key=secret"):
            with self.subTest(url=url):
                self.write("mcp.json", json.dumps({"$schema": package.SCHEMA_ROOT + "mcp.schema.json", "mcpServers": {"solar-system-db": {"type": "streamable-http", "url": url}}}))
                with self.assertRaises(package.ValidationError):
                    package.generate(self.root)

    def test_symlinked_package_files_are_rejected(self):
        path = self.root / "skills/example/references/data-caveats.md"
        path.unlink()
        self.symlink(path, self.root / "README.md")
        with self.assertRaisesRegex(package.ValidationError, "Symlink"):
            package.build(self.root)

    def test_symlinked_directories_are_rejected(self):
        path = self.root / "skills/example/references"
        path.rename(self.root / "references")
        self.symlink(path, self.root / "references", target_is_directory=True)
        with self.assertRaisesRegex(package.ValidationError, "Symlink"):
            package.check(self.root)

    def test_generate_does_not_follow_symlinks(self):
        path = self.root / "clients/cursor.json"
        path.unlink()
        self.symlink(path, self.root / "README.md")
        with self.assertRaisesRegex(package.ValidationError, "symlink"):
            package.generate(self.root)
        self.assertEqual((self.root / "README.md").read_text(), "Public documentation\n")

    def test_build_does_not_follow_output_symlinks(self):
        output = self.root / "dist"
        self.symlink(output, self.root, target_is_directory=True)
        with self.assertRaisesRegex(package.ValidationError, "Symlink"):
            package.build(self.root)


if __name__ == "__main__":
    unittest.main()
