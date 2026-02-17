# gitignore

Manage `.gitignore` files using templates from multiple sources (GitHub, Toptal, local).

**Repository:** [github.com/polliard/gitignore](https://github.com/polliard/gitignore)

## Installation

```bash
# From source (Go 1.23+ required)
go install github.com/polliard/gitignore/src/cmd/gitignore@latest

# macOS (Apple Silicon)
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-darwin-arm64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/

# macOS (Intel)
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-darwin-amd64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/

# Linux
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-linux-amd64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/
```

## Configuration

Create `~/.gitignorerc` or `~/.config/gitignore/gitignorerc`:

```ini
# GitHub repository URL for templates
gitignore.template.url = https://github.com/github/gitignore

# Enable Toptal API as fallback source
enable.toptal.gitignore = true

# Path to local templates directory
gitignore.local-templates-path = ~/.config/gitignore/templates

# Default types for 'init' command
gitignore.default-types = github/go, github/global/macos, github/global/visualstudiocode
```

## Template Sources

Templates are searched in priority order:

1. **Local** — `~/.config/gitignore/templates/` (custom templates, highest priority)
2. **GitHub** — Repository from `gitignore.template.url`
3. **Toptal** — [gitignore.io API](https://www.toptal.com/developers/gitignore) (if enabled)

## MCP Server

As of v1.3.0, gitignore supports [Model Context Protocol](https://modelcontextprotocol.io/) via the `serve` command:

```bash
gitignore serve
```

### VS Code Integration

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "gitignore": {
      "type": "stdio",
      "command": "gitignore",
      "args": ["serve"]
    }
  }
}
```

### Protocol Details

- **Transport:** stdio (JSON-RPC 2.0)
- **Protocol Version:** 2024-11-05
- **Capabilities:** tools (with listChanged notification support)

### Testing

```bash
# Initialize connection
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | gitignore serve

# List available tools
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | gitignore serve
```

## Tools

### gitignore_list

List all available templates from all configured sources.

**CLI:** `gitignore list`

**Example prompts:**
- "Show me all available gitignore templates"
- "What gitignore templates can I use?"

**Output format:**
```
github/actionscript
github/go
github/global/macos
github/global/visualstudiocode
local/myproject
toptal/rust
```

---

### gitignore_search

Search templates by name pattern.

**CLI:** `gitignore search <pattern>`

**Parameters:**
| Name      | Type   | Required | Description                                  |
| --------- | ------ | -------- | -------------------------------------------- |
| `pattern` | string | ✓        | Search pattern (e.g., 'rust', 'node', 'mac') |

**Example prompts:**
- "Search for rust gitignore templates"
- "Find gitignore templates for macOS"
- "What Node.js templates are available?"

**Example:**
```bash
$ gitignore search rust
github/rust
toptal/rust
toptal/rust-analyzer
```

---

### gitignore_add

Add a gitignore template to `.gitignore`. Templates are wrapped in section markers (`### START: <type>` / `### END: <type>`) for selective removal.

**CLI:** `gitignore add <type>`

**Parameters:**
| Name   | Type   | Required | Description                         |
| ------ | ------ | -------- | ----------------------------------- |
| `type` | string | ✓        | Template name or `source/name` path |

**Example prompts:**
- "Add Go gitignore patterns"
- "Add the macOS global gitignore"
- "Add github/go and github/global/visualstudiocode to my gitignore"

**Examples:**
```bash
gitignore add go                        # Auto-selects by priority
gitignore add github/go                 # Specific source
gitignore add github/global/macos       # Global templates
gitignore add local/myproject           # Custom local template
```

**Result in `.gitignore`:**
```gitignore
### START: Go
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
...
### END: Go
```

---

### gitignore_delete

Remove a previously added template section from `.gitignore`.

**CLI:** `gitignore delete <type>`

**Parameters:**
| Name   | Type   | Required | Description                |
| ------ | ------ | -------- | -------------------------- |
| `type` | string | ✓        | Template section to remove |

**Example prompts:**
- "Remove the Go gitignore patterns"
- "Delete the Node.js section from my gitignore"

**Example:**
```bash
gitignore delete go
```

---

### gitignore_ignore

Add paths/patterns directly without using a template. Useful for project-specific files.

**CLI:** `gitignore ignore <patterns...>`

**Parameters:**
| Name       | Type          | Required | Description     |
| ---------- | ------------- | -------- | --------------- |
| `patterns` | array[string] | ✓        | Patterns to add |

**Example prompts:**
- "Add /dist/ to my gitignore"
- "Ignore node_modules and *.log files"
- "Add .env.local to gitignore"

**Examples:**
```bash
gitignore ignore /dist/
gitignore ignore node_modules *.log tmp/
gitignore ignore .env.local .env.*.local
```

---

### gitignore_remove

Remove patterns previously added via `ignore`.

**CLI:** `gitignore remove <patterns...>`

**Parameters:**
| Name       | Type          | Required | Description        |
| ---------- | ------------- | -------- | ------------------ |
| `patterns` | array[string] | ✓        | Patterns to remove |

**Example prompts:**
- "Remove /dist/ from my gitignore"
- "Stop ignoring node_modules"

**Example:**
```bash
gitignore remove /dist/ node_modules
```

---

### gitignore_init

Initialize `.gitignore` with all default types from configuration.

**CLI:** `gitignore init`

**Example prompts:**
- "Initialize my gitignore with defaults"
- "Set up gitignore for this new project"

Adds all templates listed in `gitignore.default-types` configuration.

## Common Workflows

### New Go Project

```bash
gitignore add github/go
gitignore add github/global/macos
gitignore add github/global/visualstudiocode
```

Or configure defaults and run:
```bash
gitignore init
```

### Multi-Language Monorepo

```bash
gitignore add github/go
gitignore add github/node
gitignore add github/python
gitignore add github/global/macos
gitignore ignore /dist/ /build/ .env.local
```

### Custom Templates

1. Create local template:
   ```bash
   mkdir -p ~/.config/gitignore/templates
   cat > ~/.config/gitignore/templates/mycompany.gitignore << 'EOF'
   # Company-specific ignores
   .internal/
   *.secret
   .env.local
   EOF
   ```

2. Use in any project:
   ```bash
   gitignore add mycompany
   # or explicitly:
   gitignore add local/mycompany
   ```

### Audit & Cleanup

Remove templates you no longer need:
```bash
gitignore delete python
gitignore remove *.log
```

