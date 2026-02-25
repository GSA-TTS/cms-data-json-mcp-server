from fastmcp import FastMCP 
from datajson.tools import register_tools
from starlette.responses import JSONResponse

mcp = FastMCP("datajson")

register_tools(mcp)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})

app = mcp.http_app(stateless_http=True)

if __name__ == "__main__":
    mcp.run(transport="stdio")