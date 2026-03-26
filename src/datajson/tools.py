from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context

from datajson.models import SearchParams
from datajson.utils import query_dataset, clean_up_inventory, parse_dataset_details_page


def register_tools(mcp):
    @mcp.tool(task=True)
    async def search_datasets(params:SearchParams):
        '''
        searches data inventory on data.medicaid.gov 

        ARGS:
            params: search paramters for query
        '''
        url = 'https://data.medicaid.gov/data.json' 

        params_dict = params.to_url() 
        if params_dict is not None: 
            params_str = "&".join([f'{k}={v}' for k,v in list(params_dict.items())])

            url = f"{url}?{params_str}"

        results = await query_dataset(url)
        return clean_up_inventory(results, limit=params.size)


    @mcp.tool(task=True)
    async def get_candidate_datasets(inventory:dict, 
                                     ctx:Context = CurrentContext(), 
                                     limit:int|None = 15) -> list[dict]:
        '''
        retrieve details on datasets matching search specifications
        this tool allows you get to get column/variable level information

        use the context from the current session to decide which datasets 
        are relevant to the users question

        ARGS:
            inventory: dictionary containing data.medicaid.gov's data.json inventory
            context: context from current session
            limit: number of individual datasets to inspect 
        '''
        if inventory is None:
            raise Exception('Query returned no datasets')
        
        candidates = []

        if limit is None:
            limit = len(inventory) - 1

        titles = list(inventory.keys())
        
        # for _, dataset in list(inventory.items())[:limit]:
        #     url = dataset.get('datasetDetails')
        
        for i in range(len(list(inventory.keys())))[:limit]:
            dataset = inventory[titles[i]]
            url = dataset.get('datasetDetails')

            if limit > 20 and i % 10 == 0:
                await ctx.report_progress(progress=i, total=limit)

            if url is not None: 
                try:
                    results = await query_dataset(url)
                    results = parse_dataset_details_page(results)
                    candidates.append(results)
                except:
                    continue

        return candidates


