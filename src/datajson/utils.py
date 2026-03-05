import httpx
from datajson.models import SearchParams


def format_inventory_search(params:SearchParams) -> str:
    base_url = 'https://data.medicaid.gov/data.json' 
    params_dict = params.to_url()
    if params_dict is not None:
        params_str = "&".join([f'{k}={v}' for k,v in list(params_dict.items())])
        return  f"{base_url}?{params_str}"
    else:
        return base_url
    

async def query_dataset(url:str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=180) as client: 
            response = await client.get(
                    url
                )
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        raise Exception(f'query failed: {e}') 
    

def clean_up_inventory(inventory:dict, 
                       limit:int|None=None) -> dict:
        '''
        helper function to clean up retrived inventory 
        from data.medicaid.gov 
        '''
        datasets = inventory.get('dataset')
        if datasets is None:
            raise Exception('Query returned no datasets')
        
        cleaned_inventory = {}

        if limit is None:
                limit = len(datasets) - 1
        
        for dataset in datasets[:limit]: 
            title = dataset.get('title')

            distributions = dataset.get('distribution', {})
            dataset_url = None
            for distribution in distributions:
                 if 'describedBy' in list(distribution.keys()):
                      dataset_url = distribution['describedBy']

            if title is not None: 
                cleaned_inventory[title] = {
                    'description': dataset.get('description'), 
                    'accrualPeriodicity': dataset.get('accrualPeriodicity'), 
                    'originallyPublished': dataset.get('issued'), 
                    'lastUpdated': dataset.get('modified'), 
                    'themes': dataset.get('theme'), 
                    'keywords': dataset.get('keyword'), 
                    'datasetDetails': dataset_url
                }
        return cleaned_inventory