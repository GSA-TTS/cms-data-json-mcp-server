from fastmcp import Context 
import httpx 
from datajson.models import SearchParams
from datajson.utils import query_dataset, clean_up_inventory


def register_tools(mcp):
    @mcp.tool()
    async def search_datasets(params:SearchParams):
        '''
        searches data inventory on data.medicaid.gov 


        ARGS:
            params: search paramters for query
        '''
        url = 'https://data.medicaid.gov/data.json' 

        params_dict = params.to_url() 
        if params_dict is not None: 
            params = "&".join([f'{k}={v}' for k,v in list(params_dict.items())])

            url = f"{url}?{params}"

        results = await query_dataset(url)
        return clean_up_inventory(results)


    @mcp.tool()
    async def get_candidate_datasets(inventory:dict, 
                                     limit:int|None = 10) -> list[dict]:
        '''
        retrieve details on datasets matching search specifications

        ARGS:
            inventory: dictionary containing data.medicaid.gov's data.json inventory
            limit: number of individual datasets to inspect 
        '''
        datasets = inventory.get('dataset', None)

        if datasets is None:
            raise Exception('Query returned no datasets')
        
        
        candidates = []

        if limit is None:
            limit = len(datasets) - 1

        for dataset in datasets[:limit]:
            distributions = dataset.get('distribution')
            for distribution in distributions:
                url = distribution.get('describedBy')

                if url is not None: 
                    results = await query_dataset(url)
                    candidates.append(results)
        return candidates


