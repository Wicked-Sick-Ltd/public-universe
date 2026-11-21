"""Cloud-agent docs must match when install.sh reaches the package mirror."""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class CloudAgentEnvironmentTests(unittest.TestCase):
    def test_docs_distinguish_conditional_apt_from_offline_commands(self):
        agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        install = (REPO / ".cursor/install.sh").read_text(encoding="utf-8")
        marker = "## Cloud agent environment"
        self.assertIn(marker, agents)
        body = agents.split(marker, 1)[1]

        uses_package_mirror = "import ensurepip" in install and "apt-get update" in install
        self.assertTrue(uses_package_mirror)
        self.assertLess(install.index("import ensurepip"), install.index("apt-get update"))
        self.assertLess(install.index("apt-get update"), install.index("python3 -m venv"))

        self.assertNotIn("Install, packaging, and the test suite stay offline", body)
        self.assertIn("Packaging and the test suite stay offline", body)
        self.assertIn("do not call the remote MCP endpoint", body)
        self.assertIn("Creating `.venv` is offline when `ensurepip` is already present.", body)
        self.assertIn("When `ensurepip` is missing", body)
        self.assertIn("apt-get update", body)
        self.assertIn("package mirror", body)


if __name__ == "__main__":
    unittest.main()
