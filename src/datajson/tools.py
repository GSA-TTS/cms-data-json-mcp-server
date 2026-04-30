from typing import Any

from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
from datajson.utils import query_dataset, parse_dataset_details_page, _tokenize_text


def register_tools(mcp):
    @mcp.tool(task=True)
    async def datajson_search_inventory(query:str, 
                                        ctx:Context=CurrentContext(),
                                        k:int=10):
        '''
        searches data inventory on data.medicaid.gov with 
        simple BM25 search - surfaces relevant candidates
        for LLM to evaluate

        use this to discover datasets that are potentially  
        relevant to a users query. feel free to add synonyms 
        or other relevant terms to the users query to surface 
        more results

        ARGS:
            query: question the user has
            ctx: context from current session
            k: number of results to return
                - use default unless specified overwise
                - will return fewer than 'k' candidates if there are <k
                  datasets will positive relevancy scores
        '''
        bm25 = ctx.lifespan_context['bm25']
        inventory = ctx.lifespan_context['inventory']

        dataset_scores = bm25.get_scores(_tokenize_text(query))
        ranked_scores = sorted(enumerate(dataset_scores), key=lambda s: s[1], reverse=True)

        datasets = list(inventory.keys())
        candidates = {}
        for idx, score in ranked_scores[:k]:
            if score <= 0:
                break 
            candidates[datasets[idx]] = inventory[datasets[idx]]

        return candidates

    @mcp.tool(task=True)
    async def datajson_search_datasets(inventory:dict[str, Any], 
                                       ctx:Context=CurrentContext(), 
                                       limit:int|None=20) -> list[dict]:
        '''
        retrieve details on datasets matching search specifications
        this tool allows you get to get column/variable level information

        use the context from the current session to decide which datasets 
        are relevant to the users question through the datajson_search_inventory
        function. DO NOT PASS IN THE ENTIRE INVENTORY - only search details for a subset of datasets

        use this whenever asked about column/variable level information

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