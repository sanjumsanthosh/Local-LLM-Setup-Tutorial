import json
import os

import requests
from langchain.tools import tool
from icecream import ic

from duckduckgo_search import DDGS

class SearchTools:

    @staticmethod
    def search_using_DDGS(query):
        ddgs = DDGS()
        results = ddgs.text(query, region='wt-wt', max_results=5)
        return results
        import json
    import logging
    
    
    @staticmethod
    def try_sanitizing_query(query):
        ic("Received query: - ", query)
        
        # Check if the query is JSON parsable and contains a 'title'
        try:
            query_json = json.loads(query)
            ic("Parsed JSON: - ", query_json)
            
            if 'title' in query_json:
                ic("Found 'title' in JSON: - ", query_json['title'])
                return query_json['title']
            elif 'query' in query_json and 'title' in query_json['query']:
                ic("Found 'title' in 'query': - ", query_json['query']['title'])
                return query_json['query']['title']
            elif 'website' in query_json:
                if isinstance(query_json['website'], dict) and 'title' in query_json['website']:
                    ic("Found 'title' in 'website': - ", query_json['website']['title'])
                    return query_json['website']['title']
                elif isinstance(query_json['website'], str):
                    ic("Found 'website' as string: - ", query_json['website'])
                    return query_json['website']
        except json.JSONDecodeError:
            ic("Failed to parse query as JSON")
        
        # Check if the query is a direct title
        if isinstance(query, str) and query.strip():
            ic("Query is a direct title: - ", query.strip())
            return query.strip()
        
        # Add more checks here as needed
        
        # If all checks fail, return the original query as string
        ic("Returning original query as string: - ", str(query))
        return str(query)

    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
        about a given topic and return relevant results"""
        query = SearchTools.try_sanitizing_query(query)
        results = SearchTools.search_using_DDGS(query)
        string = []
        for result in results:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['href']}",
                    f"Snippet: {result['body']}", "\n-----------------"
                ]))
            except KeyError:
                continue

        return '\n'.join(string)
