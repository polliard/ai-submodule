# Tool Setup Procedure

> Standard bootstrap sequence for all personas. Execute at the start of every analysis session.

## Prerequisites

- Ensure a package manager is available (`brew` on macOS, `apt` on Debian/Ubuntu)
- Create a Python virtual environment for pip installs: `python -m venv .persona-tools && source .persona-tools/bin/activate`
- Use `npx` for Node.js CLI tools when possible to avoid global installs

## Bootstrap Steps

1. **Check** — Run `command -v <tool>` for each required tool to determine what is already installed
2. **Install** — For missing tools, execute the install command from the persona's Allowed Tools list. Install required tools first; skip supplementary tools if time or resources are constrained
3. **Verify** — Run `<tool> --version` to confirm each installation is functional
4. **Adapt** — If a required tool cannot be installed (platform, permissions, network):
   - Document the specific constraint
   - Note which evaluation criteria are affected
   - If >50% of required tools are unavailable, declare the persona degraded and flag this in output
5. **Report** — Emit a tool status summary before beginning analysis:

   ```
   Tool Status:
   ✓ semgrep (v1.56.0) [required]
   ✗ trivy — brew not available [supplementary]
   ```

## Platform Notes

- `brew install` commands are macOS-specific. On Linux, substitute `apt install`, `dnf install`, or direct binary downloads
- `pip install` commands must always run inside a virtual environment
- Prefer `npx <tool>` over `npm install -g <tool>` for one-shot tool execution
- Tools marked "Manual setup" require platform-specific installation or commercial licenses and should not be auto-installed

## Tool Classification

- **Required** — Essential for the persona's core evaluation. Analysis is degraded without these.
- **Supplementary** — Enhances analysis but the persona can function without them.
- **Manual setup** — Cannot be auto-installed (GUI tools, commercial software, platform-native). Note availability and skip during bootstrap.
