# data.cms.gov data.json MCP server

Disclaimer: This server is a proof of concept and is for demonstration purposes only.

## Overview
This server helps users navigate data resources available on data.medicaid.gov using it's data.json file, which an inventory of all data assets available on the site. 

The most common workflow is to:
1) pull the data.json file using the server
2) identify a broad set of candidate datasets 
2) drill down into column level details on each candidate 

The server enables this with the following tools
- **search_datasets:** search inventory 
- **get_candidate_datasets:** pull details for a particular dataset