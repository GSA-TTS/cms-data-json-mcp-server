import asyncio
from datajson.utils import _build_index
from fastmcp import FastMCP 
from fastmcp.server.lifespan import lifespan
from datajson.tools import register_tools
from starlette.requests import Request
from starlette.responses import JSONResponse

@lifespan
async def server_lifespan(app):
    inventory, corpus, bm25 = await asyncio.wait_for(
        _build_index(), timeout=45
    )
    yield {'index':True, 
           'inventory':inventory, 
           'corpus':corpus,
           'bm25':bm25} 

mcp = FastMCP(name="datajson", 
              instructions="""
              This server is for searching for data assets on 
              data.medicaid.gov
              
              Any questions related to Medicaid/CHIP data MUST use this server

              Here are some of the kinds of data available on data.medicaid.gov:
              - prescription drug utilization 
              - drug rebate programs
              - state eligibility rules 
              - quality measures
              - managed care enrollment 
              - monthly state level enrollment 

              These are just a few examples and is not an exhaustive 
              list of the data available 

              MOST COMMON WORK FLOW:
              - pull the data inventory using search_datasets
              - model makes a judgement about which datasets might be relevant
              - investigate relevant datasets using get_candidate_datasets to see column-levle information
              """, 
              lifespan=server_lifespan)

register_tools(mcp)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request:Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "service": "cms-datajson-mcp-server"})

app = mcp.http_app(stateless_http=True)

if __name__ == "__main__":
    mcp.run(transport="stdio")