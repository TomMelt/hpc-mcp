# hpc-mcp :zap::computer:

This project provides MCP tools for HPC. These are designed to integrate with LLMs. My initial plan
is to integrate with LLMs called from IDEs such as [cursor](https://cursor.com/) and
[vscode](https://code.visualstudio.com/).

## Quick Start Guide :rocket:

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and installation.
If you don't have uv installed, follow [installation
instructions](https://docs.astral.sh/uv/getting-started/installation/) on their website.

Once we have `uv` installed we can install the dependencies and run the tests with the following
command:

```bash
uv run --dev pytest
```

### Adding the MCP Server
#### Cursor

1. Open Cursor and go to settings.
2. Click `Tools & Integrations`
3. Click `Add Custom MCP`

> [!NOTE]
> This will open your system-wide MCP settings (`$HOME/.cursor/mcp.json`). If you prefer to set this
> on a project-by-project basis, then you can create a local configuration using
> `<path/to/project/root>/.cursor/mcp.json`.

4. Add the following configuration:

```json
{
  "mcpServers": {
    "hpc-mcp": {
      "command": "uv",
      "args": [
                "--directory",
                "<path/to>/hpc-mcp",
                "run",
                "src/debug.py"
            ]
    }
  }
}
```

#### VSCode

1. Open command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>) and select `MCP: Add Server...`

![add MCP server](./imgs/vscode/step_1_command.png)

2. Choose the option `command (stdio)` since the server will be run locally
3. Type the command to run the MCP server:
```bash
uv --directory <path/to>/hpc-mcp run src/debug.py
```
4. Select reasonable name for the server e.g. "HpcMcp" (camel case is a convention)
5. Select whether to add the server locally or globally.
6. You can tune the settings by opening `setting.json` (global settings) or `.vscode/setting.json` (workspace settings)

![add MCP server](./imgs/vscode/json_settings.png)

#### Zed

1. Open [Zed](https://zed.dev/) and go to settings.
2. Open general settings `CTRL-ALT-C`
3. Under section Model Context Protocol (MCP) Servers click `Add Custom Server`
4. Add the following text (changing the `<path/to>/hpc-mcp` to your actual path)

```json
{
  /// The name of your MCP server
  "hpc-mcp": {
    /// The command which runs the MCP server
    "command": "uv",
    /// The arguments to pass to the MCP server
    "args": [
      "--directory",
      "<path/to>/hpc-mcp",
      "run",
      "src/debug.py"
    ],
    /// The environment variables to set
    "env": {}
  }
}
```

### Test the MCP Server

Test the MCP using our simple example
- open terminal
- `cd example/simple`
- build the example using `make`
- this should generate `segfault.exe`
- then type the following prompt into your IDE LLM agent
```
"debug a crash in the program examples/simple/segfault.exe"
```
- this should ask your permission to run `debug_crash` MCP tool
- accept and you should get a response like the following
![cursor-demo](./imgs/cursor-demo.png)

## Running local LLMs with Ollama

To run the `hpc-mcp` MCP tool with a local Ollama model use the Zed text editor. It should
automatically detect local running ollama models and make them available. As long as you have
installed the `hpc-mcp` MCP server in zed (see instructions [here](###-test-the-mcp-server)) it
should be available to your models. For more info on ollama integration with zed see zed's
[documentation](https://zed.dev/docs/ai/configuration#ollama).

> [!NOTE]
> Not all models support calling of MCP tools. I managed to have success with
> [`qwen3:latest`](https://ollama.com/library/qwen3:latest).

## Core Dependencies

- `python`
- `uv`
- `fastmcp`
