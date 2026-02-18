# Credential Policy

> Follow this policy when using tools that require authentication (cloud CLIs, SaaS APIs, cluster access).

## Rules

1. **Never hardcode credentials** — Do not embed API keys, tokens, passwords, or secrets in commands, scripts, or output
2. **Use environment variables** — Source credentials from environment variables (e.g., `AWS_PROFILE`, `KUBECONFIG`, `WANDB_API_KEY`)
3. **Minimum privilege** — Request only the permissions needed for the specific analysis. Use read-only roles where possible
4. **No logging of secrets** — Ensure tool output and tool status reports do not contain credentials
5. **Scoped sessions** — Use temporary credentials (STS tokens, short-lived tokens) when available
6. **Prompt, don't store** — If credentials must be provided interactively, never write them to disk, shell history, or log files

## Tools Requiring Credentials

| Tool | Credential Type | Provision Method |
|------|----------------|------------------|
| AWS CLI | AWS profile or access keys | `AWS_PROFILE` environment variable |
| Azure CLI | Azure subscription | `az login` (interactive) |
| gcloud | GCP project | `gcloud auth login` (interactive) |
| kubectl | Kubeconfig | `KUBECONFIG` environment variable |
| Weights & Biases | API key | `WANDB_API_KEY` environment variable |
| PagerDuty CLI | API token | `PD_TOKEN` environment variable |
| GitHub CLI | OAuth token | `gh auth login` (interactive) |
