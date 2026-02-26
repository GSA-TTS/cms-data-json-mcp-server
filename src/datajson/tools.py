from fastmcp import Context 
import httpx 
from datajson.models import SearchParams


def register_tools(mcp):
    @mcp.tool()
    async def search_datasets(params:SearchParams):
        url = 'https://data.medicaid.gov/data.json' 

        params_dict = params.to_url() 
        if params_dict is not None: 
            params = "&".join([f'{k}={v}' for k,v in list(params_dict.items())])

            url = f"{url}?{params}"

        try:
            async with httpx.AsyncClient(timeout=180) as client: 
                response = await client.get(
                        url
                    )
                response.raise_for_status()
                return response.json()
            
        except Exception as e:
            raise Exception(f'query failed: {e}')

