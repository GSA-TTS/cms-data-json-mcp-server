from typing import Any

from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
from datajson.utils import query_dataset, clean_up_inventory, parse_dataset_details_page


def register_tools(mcp):
    @mcp.tool(task=True)
    async def datajson_search_inventory() -> dict[str, Any]:
        '''
        searches data inventory on data.medicaid.gov 

        use this to discover datasets that are potentially  
        relevant to a users query
        '''
        url = 'https://data.medicaid.gov/data.json' 

        results = await query_dataset(url)
        return clean_up_inventory(results)


    @mcp.tool(task=True)
    async def datajson_search_datasets(inventory:dict[str, Any], 
                                    ctx:Context = CurrentContext(), 
                                    limit:int|None = 20) -> list[dict]:
        '''
        retrieve details on datasets matching search specifications
        this tool allows you get to get column/variable level information

        use the context from the current session to decide which datasets 
        are relevant to the users question. DO NOT PASS IN THE ENTIRE INVENTORY - 
        only search details for a subset of datasets

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
    

    @mcp.tool(task=True)
    async def datajson_summarize_datasets(candidates:list[dict]):
        '''
        
        '''
        pass 