# data.cms.gov/data.json MCP server
Disclaimer: This server is a proof of concept and is for demonstration purposes only. While this prototype is meant to be a proof of concept for data.cms.gov, please note that it currently searches **data.medicaid.gov.**

## Overview
This server helps users navigate data resources available on data.medicaid.gov using it's data.json file, which an inventory of all data assets available on the site. 

Upon start up, the server creates a light-weight BM25 index of the current data inventory, which is used to 
surface relevant candidates for the LLM to inspect. Combining traditional search with AI systems natural language 
understanding capabilities allows the model to investigate a more targetted subset of dataset and avoids overwhelming the session's context window. 

#### Most common workflow
1) run an initial search against the indexed inventory 
2) identify a broad set of relevant datasets 
2) drill down into column level details

#### Available tools
- **datajson_search_inventory:** search inventory 
- **datajson_search_datasets:** pull details for a particular dataset

## Running Locally
To run a copy of this server locally, use the following commands:

```
git clone https://github.com/GSA-TTS/cms-data-json-mcp-server
cd cms-data-json-mcp-server
uv sync --dev
uv run src/datajson/app.py
```

## Claude Desktop Setup 
1. Open your Claude config file 

2. Add the path to your local installation
```
{
  "mcpServers": {
    "cms-data-json": {
      "command": "/path/to/data-json-mcp-pilot"
    }
  }
}
```

## Repository Structure 
```
src/
    datajson/
        app.py       # set up MCP app
        models.py    # field definitions
        tools.py     # mcp tools
        utils.py     # helper functions
manifest.yaml         # cloud.gov deployment config
pyproject.toml
```