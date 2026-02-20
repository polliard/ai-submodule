# Base Tools

> These tools are commonly needed across multiple personas.
> Install once per session and share across participants
> during panel reviews.

## Shared Tool Set

| Tool | Install (macOS) | Install (Linux) | Purpose |
| --- | --- | --- | --- |
| jq | `brew install jq` | `apt install -y jq` | Parse JSON logs and API responses |
| Semgrep | `pip install semgrep` | `pip install semgrep` | Static analysis for security patterns |
| k6 | `brew install k6` | `snap install k6` | Load testing and performance benchmarks |
| cloc | `brew install cloc` | `apt install -y cloc` | Count lines of code and codebase metrics |
| Trivy | `brew install trivy` | `apt install -y trivy` | Vulnerability scanning (containers, deps) |
| Madge | `npx madge` | `npx madge` | JS/TS dependency graph visualization |
| Lighthouse | `npx lighthouse` | `npx lighthouse` | Web performance and accessibility audit |
| Mermaid CLI | `npx @mermaid-js/mermaid-cli` | `npx @mermaid-js/mermaid-cli` | Diagram generation |

## Usage

- If a persona lists these tools, they need not be reinstalled if already available
- During panel reviews, install base tools once during first bootstrap and reuse
- Base tools are **supplementary** unless a persona explicitly marks them as required
