import httpx 
from datajson.models import SearchParams


async def format_inventory_search(params:SearchParams) -> str:
    base_url = 'https://data.medicaid.gov/data.json' 
    params_dict = params.to_url()
    if params_dict is not None:
        params_str = "&".join([f'{k}={v}' for k,v in list(params_dict.items())])
        return  f"{base_url}?{params_str}"
    else:
        return base_url


# async def query_dataset(url:str) -> dict:
#     try:
#         async with httpx.AsyncClient(timeout=180) as client: 
#             response = await client.get(
#                     url
#                 )
#             response.raise_for_status()
#             return response.json()
            
#     except Exception as e:
#         raise Exception(f'query failed: {e}') 


