from fastmcp import FastMCP 
from datajson.tools import register_tools
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP(name="datajson", 
              instructions="""
              This server is for searching for data assets on 
              data.medicaid.gov. Any questions related to Medicaid/CHIP 
              data should attempt to use this server. 

              Here are some of the kinds of data available on data.medicaid.gov:
              - prescription drug utilization 
              - state eligibility rules 
              - quality measures
              - managed care enrollment 
              - monthly state level enrollment 

              These are just a few examples and are not all encompassing
              of the kinds of data available 
              """)

register_tools(mcp)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request:Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "service": "cms-datajson-mcp-server"})


app = mcp.http_app(stateless_http=True)

if __name__ == "__main__":
    mcp.run(transport="stdio")