import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from icecream import ic


class BrowserTools():


  def scrape_webpage(url):
    ic("Scraping webpage: - ", url)
    response = requests.get(url)
    if response.status_code == 200:
        ic("Successfully fetched the webpage")
        soup = BeautifulSoup(response.content, 'html.parser')
        text =  soup.get_text()
        remove_chars = ['\n', '\t', '\r', '\xa0']
        for char in remove_chars:
            text = text.replace(char, '')
        # remove extra spaces
        text = ' '.join(text.split())
        return text
    else:
        ic("Failed to fetch the webpage")
        raise Exception(f"Failed to fetch the webpage: {url}")
    

  @staticmethod
  def try_sanitizing_query(query):
    ic("Received query: - ", query)
    try:
        query_json = json.loads(query)
        ic("Parsed JSON: - ", query_json)
        if 'title' in query_json:
            ic("Found title in query_json: - ", query_json['title'])
            return query_json['title']
        elif 'query' in query_json and 'title' in query_json['query']:
            ic("Found title in nested query_json: - ", query_json['query']['title'])
            return query_json['query']['title']
        elif 'website' in query_json:
            if isinstance(query_json['website'], dict) and 'title' in query_json['website']:
                ic("Found title in website dict: - ", query_json['website']['title'])
                return query_json['website']['title']
            elif isinstance(query_json['website'], str):
                ic("Found website as string: - ", query_json['website'])
                return query_json['website']
    except json.JSONDecodeError:
        ic("Failed to parse JSON, treating query as a direct title")

    # Check if the query is a direct title
    if isinstance(query, str) and query.strip():
        ic("Query is a direct title: - ", query.strip())
        return query.strip()
    
    # If all checks fail, return the original query as string
    ic("Returning original query as string: - ", str(query))
    return str(query)


  @tool("Scrape website content based on the given URL")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content based on the given URL"""
    website = BrowserTools.try_sanitizing_query(website)
    content = BrowserTools.scrape_webpage(website)
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing researches and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
