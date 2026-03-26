# data.cms.gov/data.json MCP server

Disclaimer: This server is a proof of concept and is for demonstration purposes only. While this prototype is meant to be a proof of concept for data.cms.gov, please note that it currently searches **data.medicaid.gov.**

## Overview
This server helps users navigate data resources available on data.medicaid.gov using it's data.json file, which an inventory of all data assets available on the site. 

The most common workflow is to:
1) pull the data.json file using the server
2) identify a broad set of relevant datasets 
2) drill down into column level details

The server enables this with the following tools:
- **search_datasets:** search inventory 
- **get_candidate_datasets:** pull details for a particular dataset