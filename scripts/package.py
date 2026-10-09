#!/usr/bin/env python3
"""Generate client examples and deterministic, allowlisted PublicUniverse plugin archives.

Requires Python 3.11+. No network access, dependencies, or client configuration writes.
Validation enforces this repository's structural contract, not general JSON Schema.
Frontmatter validation deliberately supports this repository's small YAML subset,
not arbitrary YAML: name, description (plain/quoted/folded), metadata.version.
"""

import argparse
import json
import re
import tomllib
import zipfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("docs/clients.md", "docs/openai.md", "docs/validation.md", "docs/submission.md", "docs/listings.md")
REGISTRY_SCHEMA = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"
REGISTRY_NAME = "net.publicuniverse/publicuniverse"
REGISTRY_DESCRIPTION = "Free astronomy catalogue: solar system objects, sky positions, close approaches and more."
SCHEMA_ROOT = "https://agent-plugins.org/schemas/1.0.0/"


class ValidationError(ValueError):
    pass


def read_file(root, relative):
    path = root / relative
    if Path(relative).is_absolute() or not path.is_relative_to(root):
        raise ValidationError(f"Path outside package: {relative}")
    if ".." in Path(relative).parts:
        raise ValidationError(f"Parent path is not allowed: {relative}")
    current = path
    while current != root:
        if current.is_symlink():
            raise ValidationError(f"Symlink is not allowed: {relative}")
        current = current.parent
    if not path.is_file():
        raise ValidationError(f"Missing package file: {relative}")
    return path.read_bytes()


def load_json(root, relative):
    try:
        return json.loads(read_file(root, relative))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"Invalid JSON in {relative}: {error}") from error


def canonical(root):
    plugin = load_json(root, "plugin.json")
    mcp = load_json(root, "mcp.json")
    if not isinstance(plugin, dict) or plugin.get("$schema") != SCHEMA_ROOT + "plugin.schema.json":
        raise ValidationError("plugin.json must declare the Agent Plugins 1.0.0 schema")
    allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
    if set(plugin) - allowed:
        raise ValidationError(f"Unsupported plugin metadata: {', '.join(sorted(set(plugin) - allowed))}")
    if not isinstance(plugin.get("name"), str) or len(plugin["name"]) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plugin["name"]):
        raise ValidationError("Plugin name must be a lowercase slug of at most 64 characters")
    if not isinstance(plugin.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", plugin["version"]):
        raise ValidationError("Plugin version must use major.minor.patch")
    for key in ("description", "repository", "license"):
        if not isinstance(plugin.get(key), str) or not plugin[key].strip():
            raise ValidationError(f"Missing plugin metadata: {key}")
    if "homepage" in plugin and (not isinstance(plugin["homepage"], str) or not plugin["homepage"].strip()):
        raise ValidationError("Plugin homepage must be a nonempty string")
    if "author" in plugin:
        author = plugin["author"]
        if not isinstance(author, dict) or set(author) - {"name", "email", "url"}:
            raise ValidationError("Plugin author must be an object with name and optional email/url")
        if "name" not in author or any(not isinstance(value, str) or not value.strip() for value in author.values()):
            raise ValidationError("Plugin author name, email and URL must be nonempty strings")
    if "keywords" in plugin:
        keywords = plugin["keywords"]
        if not isinstance(keywords, list) or any(not isinstance(value, str) or not value.strip() for value in keywords):
            raise ValidationError("Plugin keywords must be a list of nonempty strings")
    if "extensions" in plugin:
        extensions = plugin["extensions"]
        if not isinstance(extensions, dict) or any(not isinstance(value, dict) for value in extensions.values()):
            raise ValidationError("Plugin extensions must be an object containing vendor objects")
    if not isinstance(mcp, dict) or mcp.get("$schema") != SCHEMA_ROOT + "mcp.schema.json":
        raise ValidationError("mcp.json must declare the Agent Plugins 1.0.0 schema")
    if set(mcp) - {"$schema", "mcpServers"}:
        raise ValidationError(f"Unsupported MCP metadata: {', '.join(sorted(set(mcp) - {'$schema', 'mcpServers'}))}")
    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise ValidationError("mcp.json must provide at least one MCP server")
    for name, server in servers.items():
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise ValidationError(f"Invalid server name: {name}")
        if not isinstance(server, dict) or set(server) != {"type", "url"} or server["type"] != "streamable-http":
            raise ValidationError(f"{name}: expected a public streamable-http URL without credentials")
        if not isinstance(server["url"], str):
            raise ValidationError(f"{name}: URL must be a string")
        parsed = urlparse(server["url"])
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValidationError(f"{name}: expected an HTTPS URL without credentials, query or fragment")
    return plugin, servers


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def generated_files(root):
    plugin, servers = canonical(root)
    http = {name: {"type": "http", "url": server["url"]} for name, server in servers.items()}
    codex = "\n".join(f'[mcp_servers.{name}]\nurl = {json.dumps(server["url"])}\n' for name, server in servers.items())
    tomllib.loads(codex)
    repository = plugin["repository"].removesuffix(".git") + ".git"
    return {
        ".claude-plugin/plugin.json": json_bytes({key: value for key, value in plugin.items() if key not in ("$schema", "extensions")}),
        ".mcp.json": json_bytes({"mcpServers": http}),
        "gemini-extension.json": json_bytes({
            "name": plugin["name"], "version": plugin["version"],
            "mcpServers": {name: {"httpUrl": server["url"]} for name, server in servers.items()},
        }),
        "clients/claude.json": json_bytes({"mcpServers": http}),
        "clients/codex.toml": codex.encode(),
        "clients/cursor.json": json_bytes({"mcpServers": {name: {"url": server["url"]} for name, server in servers.items()}}),
        "clients/vscode.json": json_bytes({"servers": http}),
        "clients/copilot-cli.json": json_bytes({"mcpServers": {name: {**server, "tools": ["*"]} for name, server in http.items()}}),
        ".claude-plugin/marketplace.json": json_bytes({
            "name": plugin["name"],
            "owner": {key: value for key, value in plugin.get("author", {"name": plugin["name"]}).items() if key in ("name", "email")},
            "metadata": {"description": plugin["description"], "version": plugin["version"]},
            "plugins": [{
                "name": plugin["name"], "source": "./", "description": plugin["description"], "version": plugin["version"],
                **{key: plugin[key] for key in ("author", "homepage", "repository", "license", "keywords") if key in plugin},
                "category": "education",
            }],
        }),
        "server.json": json_bytes({
            "$schema": REGISTRY_SCHEMA, "name": REGISTRY_NAME,
            "title": plugin.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("displayName", plugin["name"]),
            "description": REGISTRY_DESCRIPTION, "version": plugin["version"],
            **({"websiteUrl": plugin["homepage"]} if "homepage" in plugin else {}),
            "repository": {"url": plugin["repository"].removesuffix(".git"), "source": "github"},
            "remotes": [{"type": "streamable-http", "url": server["url"]} for server in servers.values()],
        }),
        "clients/grok.toml": "\n".join(f'[mcp_servers.{name}]\nurl = {json.dumps(server["url"])}\n' for name, server in servers.items()).encode(),
        "clients/openai-marketplace.json": json_bytes({
            "name": "publicuniverse-local", "interface": {"displayName": "PublicUniverse local preview"},
            "plugins": [{"name": plugin["name"], "source": {"source": "url", "url": repository, "ref": "main"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Education"}],
        }),
    }


def generate(root):
    for relative, content in generated_files(root).items():
        path = root / relative
        current = path
        while current != root:
            if current.is_symlink():
                raise ValidationError(f"Refusing to write through symlink: {relative}")
            current = current.parent
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def skill_files(root):
    files = set()
    skill_root = root / "skills"
    if skill_root.is_symlink():
        raise ValidationError("Symlink is not allowed: skills")
    paths = sorted(skill_root.glob("*/SKILL.md"))
    if not paths:
        raise ValidationError("No skills found")
    for path in paths:
        relative = path.relative_to(root).as_posix()
        content = read_file(root, relative).decode().replace("\r\n", "\n")
        pieces = content.split("---", 2)
        if len(pieces) != 3 or pieces[0] or not pieces[1].startswith("\n"):
            raise ValidationError(f"Missing frontmatter: {relative}")
        # Intentionally narrow: fail rather than silently interpreting other YAML.
        header = pieces[1]
        pattern = r'\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n((?:  [^\n]*\n)*)(?:metadata:\n  version: "(\d+\.\d+\.\d+)"\n)?'
        match = re.fullmatch(pattern, header)
        if not match or match[1] != path.parent.name:
            raise ValidationError(f"Unsupported frontmatter or mismatched skill name: {relative}")
        description = match[3].strip() if match[2] in (">", "|", ">-", "|-") else match[2].strip('"\' ')
        if not description or len(description) > 1024:
            raise ValidationError(f"Skill description must contain 1–1024 characters: {relative}")
        files.add(relative)
        references = path.parent / "references"
        if references.is_symlink():
            raise ValidationError(f"Symlink is not allowed: {references.relative_to(root)}")
        # These are the three reference documents shipped by this repository.
        for name in ("data-caveats.md", "audit-checklist.md", "curriculum-map.md"):
            reference = references / name
            if reference.exists() or reference.is_symlink():
                reference_relative = reference.relative_to(root).as_posix()
                read_file(root, reference_relative)
                files.add(reference_relative)
        for reference in re.findall(r"references/[a-zA-Z0-9_./-]+\.md", content):
            reference_relative = (path.parent / reference).relative_to(root).as_posix()
            read_file(root, reference_relative)
            if reference_relative not in files:
                raise ValidationError(f"Reference needs adding to package allowlist: {reference_relative}")
    return files


def check(root):
    expected = generated_files(root)
    for relative, content in expected.items():
        if read_file(root, relative) != content:
            raise ValidationError(f"Generated file drift: {relative}; run python3 scripts/package.py generate")
    files = {"plugin.json", "mcp.json", "README.md", "CHANGELOG.md", "LICENSE", "NOTICE", *DOCS, *expected, *skill_files(root)}
    interface = canonical(root)[0].get("extensions", {}).get("com.openai", {}).get("interface", {})
    for field in ("logo", "composerIcon"):
        if field in interface:
            read_file(root, interface[field])
            files.add(Path(interface[field]).as_posix())
    for relative in files:
        read_file(root, relative)
    return sorted(files)


def build(root):
    files = check(root)
    plugin, _ = canonical(root)
    output = root / "dist"
    if output.is_symlink():
        raise ValidationError("Symlink is not allowed: dist")
    output.mkdir(exist_ok=True)
    paths = [output / f'{plugin["name"]}-{plugin["version"]}{extension}' for extension in (".zip", ".plugin")]
    for path in paths:
        if path.is_symlink():
            raise ValidationError(f"Symlink is not allowed: {path.name}")
    # ZIP_STORED avoids platform/zlib variation. Both names contain the same ZIP.
    with zipfile.ZipFile(paths[0], "w", compression=zipfile.ZIP_STORED) as archive:
        for relative in files:
            entry = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, read_file(root, relative))
    paths[1].write_bytes(paths[0].read_bytes())
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "check", "build"))
    args = parser.parse_args()
    try:
        if args.command == "generate":
            generate(ROOT)
            print("Generated client examples; no user configuration was changed.")
        elif args.command == "check":
            print(f"Validated {len(check(ROOT))} package files.")
        else:
            for path in build(ROOT):
                print(path.relative_to(ROOT))
    except (ValidationError, OSError, UnicodeError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
