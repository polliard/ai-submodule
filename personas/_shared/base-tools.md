# Base Tools

> These tools are commonly needed across multiple personas. Install once per session and share across participants during panel reviews.

## Shared Tool Set

| Tool | Install (macOS) | Install (Linux) | Purpose |
|------|----------------|-----------------|---------|
| jq | `brew install jq` | `apt install -y jq` | Parse JSON logs, API responses, and structured data |
| Semgrep | `pip install semgrep` | `pip install semgrep` | Static analysis with custom rules for security and correctness patterns |
| k6 | `brew install k6` | `snap install k6` | Load testing and performance benchmarking |
| cloc | `brew install cloc` | `apt install -y cloc` | Count lines of code and quantify codebase metrics |
| Trivy | `brew install trivy` | `apt install -y trivy` | Vulnerability scanning for containers, filesystems, and dependencies |
| Madge | `npx madge` | `npx madge` | JavaScript/TypeScript dependency graph visualization |
| Lighthouse | `npx lighthouse` | `npx lighthouse` | Web performance, accessibility, and best practices auditing |
| Mermaid CLI | `npx @mermaid-js/mermaid-cli` | `npx @mermaid-js/mermaid-cli` | Diagram generation (flow, sequence, architecture) |

## Usage

- If a persona lists any of these tools, they do not need to be reinstalled if already available from a prior persona or session
- During panel reviews, install base tools once during the first participant's bootstrap and reuse for subsequent participants
- Base tools are always classified as **supplementary** unless a persona explicitly marks them as required
