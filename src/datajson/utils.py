import httpx
import regex as re
import pandas as pd
from typing import Any
from rank_bm25 import BM25Okapi

async def query_dataset(url:str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=180) as client: 
            response = await client.get(
                    url
                )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
        raise Exception(f"API request failed: {error_detail}") from e
    except httpx.RequestError as e:
        raise Exception(f"Request error: {str(e)}") from e 

def clean_up_inventory(inventory:dict[str, Any]) -> dict[str, Any]:
    '''
    helper function to clean up retrived inventory 
    from data.medicaid.gov 
    '''
    datasets = inventory.get('dataset')
    if datasets is None:
        raise Exception('Query returned no datasets')
    
    cleaned_inventory = {}
    
    for dataset in datasets: 
        title = dataset.get('title')

        # go through all distributions (most only have 1)
        distributions = dataset.get('distribution', {})
        dataset_url = None
        for distribution in distributions:
                if 'describedBy' in list(distribution.keys()):
                    dataset_url = distribution['describedBy']

        if title is not None: 
            # remove year 
            cleaned_title = re.sub(r'\d{4}', '', title).strip()

            # if title is already in inventory, only update if this is a more recent entry
            last_updated = dataset.get('modified')
            if cleaned_title in list(cleaned_inventory.keys()):
                new = pd.to_datetime(last_updated) 
                new.tz_localize(None)
                curr = pd.to_datetime(cleaned_inventory[cleaned_title]['lastUpdated'])
                curr.tz_localize(None)

                try:
                    if new < curr: 
                        continue
                except:
                        continue

            cleaned_inventory[cleaned_title] = {
                'description': dataset.get('description'), 
                'accrualPeriodicity': dataset.get('accrualPeriodicity'), 
                'originallyPublished': dataset.get('issued'), 
                'lastUpdated': last_updated, 
                'themes': dataset.get('theme'), 
                'keywords': dataset.get('keyword'), 
                'datasetDetails': dataset_url
            }
    return cleaned_inventory


def parse_dataset_details_page(dataset:dict[str, Any]) -> dict[str, Any]: 
    '''
    takes in a dataset details page and returns 
    the relevant pieces

    ARGS:
        dataset: dictionary with information on dataset fields 
        
    '''
    data = dataset.get('data')
    if not data: 
        raise Exception('No data details')
     
    fields = data.get('fields')
    if not fields: 
        raise Exception('Dataset has no fields')
     
    cleaned_fields = []
    for field in fields:
        cleaned_fields.append(
            {'title': field.get('title', ''),
             'type': field.get('type'),
             'description': field.get('description')}
          )
    return {'title': data.get('title'), 'fields': cleaned_fields}


def _tokenize_text(text:str) -> list[str]:
    '''
    tokenize text
    '''
    return re.findall(r"[a-z0-9]+", text.lower())


def _combine_dataset_text(title, data:dict[str, Any]) -> str:
    parts = [
        f"{title} " * 3,         
        data.get("description", ""),
        " ".join(data.get("keyword", [])),
        " ".join(data.get("theme", [])),
    ]
    return " ".join(parts).lower().strip()


async def _build_index() -> tuple:
    url = 'https://data.medicaid.gov/data.json' 
    inventory = await query_dataset(url)
    inventory = clean_up_inventory(inventory)
    
    corpus = [_tokenize_text(_combine_dataset_text(data, inventory.get(data, {}))) for data in inventory]
    bm25 = BM25Okapi(corpus)
    return (inventory, corpus, bm25)