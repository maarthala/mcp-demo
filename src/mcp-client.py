# Updated mcp_client.py
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()
MCP_SERVER_URL = "http://mcp-server:8000"
OLLAMA_URL = "http://ollama:11434"

class ToolRequest(BaseModel):
    prompt: str

def call_llm(prompt: str):
    """Dynamic LLM integration with Ollama"""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": f"""
            Analyze this prompt and generate tool parameters:
            {prompt}
            
            Available tools:
            - calculator (operation, a, b)
            
            Return JSON format:
            {{"tool": "tool_name", "parameters": {{...}}}}
            """,
            "format": "json",
            "stream": False
        }
    )
    return response.json()["response"]

@app.post("/process")
async def process_prompt(request: ToolRequest):
    # Get available tools
    tools = requests.get(f"{MCP_SERVER_URL}/mcp/discover").json()
    try:
        llm_raw = call_llm(request.prompt)
        llm_response = eval(llm_raw) 
    
        # Execute tool
        result = requests.post(
            f"{MCP_SERVER_URL}/mcp/execute",
            json=llm_response
        ).json()
        if "error" in result:
            raise Exception(result["error"])
        
        return {
            "original_prompt": request.prompt,
            "tool_used": llm_response["tool"],
            "operation": result["operation"],
            "result": result["content"]
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to process the prompt."
        }


if __name__ == "__main__":
    uvicorn.run("mcp-client:app", host="0.0.0.0", port=8002, reload=True)