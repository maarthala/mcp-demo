# mcp-demo
MCP demo using api microservices
## Overview

This code demonstrates how the MCP protocol works. It is not a highly optimized or sophisticated solution but provides a straightforward explanation of the protocol's functionality.

## Prerequisites

- Docker must be installed and running locally.
- `curl` command-line tool should be available.

## Usage

Run a docker-compose from root directory
```bash
docker-compose up
```

Install llama3 model into ollama

```bash
curl http://localhost:11434/api/pull -d '{"name": "llama3:latest"}'
```

To send `prompt` using this `demo`, execute the following `curl` command in your local terminal:

```bash
curl -X POST http://localhost:8002/process \
    -H "Content-Type: application/json" \
    -d '{"prompt": "add 1 and 2 ?"}'
```

### Example Output

You might not successful every request, but give a try multiple times

```json
{
    "original_prompt": "add 1 and 2 ?",
    "tool_used": "calculator",
    "operation": "+",
    "result": "3"
}
```

