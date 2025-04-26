# mcp_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from mcp import types as mcp_types
import uvicorn

app = FastAPI()

# # Tool definitions
# TOOLS = [
#     mcp_types.Tool(
#         name="calculator",
#         description="Basic arithmetic operations",
#         parameters={
#             "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
#             "a": {"type": "number"},
#             "b": {"type": "number"}
#         }
#     )
# ]


# Tool definitions
TOOLS = [
    mcp_types.Tool(
        name="calculator",
        description="Basic arithmetic operations",
        inputSchema={
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["+", "addition", "add", "subtract", "multiply", "divide"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        },
        parameters={
            "operation": {"type": "string", "enum": ["+", "addition", "add", "subtract", "multiply", "divide"]},
            "a": {"type": "number"},
            "b": {"type": "number"}
        }
    )
]


@app.get("/mcp/discover")
async def discover_tools():
    """MCP discovery endpoint"""
    return {
        "name": "Math MCP Server",
        "version": "1.0.0",
        "capabilities": TOOLS
    }

@app.post("/mcp/execute")
async def execute_tool(request: dict):
    print(request)

    try:
        """Tool execution endpoint"""
        if request["tool"] == "calculator":
            a = request["parameters"]["a"]
            b = request["parameters"]["b"]
            op = request["parameters"]["operation"]
            result = None
            if (op == "add" or op == "addition" or op == "+") : result = a + b
            elif op == "subtract": result = a - b
            elif op == "multiply": result = a * b
            elif op == "divide": result = a / b if b != 0 else "Error"
            
            return {"result": result, "content": str(result), "operation": op}
    except KeyError as e:
        return {"error": f"Missing parameter: {str(e)}"}
    
    return {"error": "Tool not found"}

if __name__ == "__main__":
    uvicorn.run("mcp-server:app", host="0.0.0.0", port=8000, reload=True)
# Run the server with: uvicorn mcp_server:app --host 127.0.0.1
