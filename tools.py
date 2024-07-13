import random
from datetime import datetime, timedelta

# Instantiate the Cohere client

import cohere
import os

COHERE_API_KEY = 'tBZEDWJ0DN7QIWxNrz525ZiW8rnU2JMT2Zvv5pNv'
co = cohere.Client(api_key=COHERE_API_KEY)

def list_calendar_events(days: int = 7, max_results: int = 10):
    print("Listing calendar events")
    # List of possible event titles
    event_titles = [
        "Team Meeting", "Project Deadline", "Lunch with Client",
        "Gym Session", "Doctor's Appointment", "Birthday Party",
        "Conference Call", "Presentation Prep", "Code Review",
        "Dentist Appointment", "Movie Night", "Grocery Shopping"
    ]
    
    # Generate random events
    events = []
    now = datetime.now()
    for _ in range(max_results):
        # Random date within the specified range
        event_date = now + timedelta(days=random.randint(0, days))
        # Random time
        event_time = timedelta(hours=random.randint(8, 20), minutes=random.choice([0, 30]))
        event_datetime = event_date.replace(hour=0, minute=0, second=0, microsecond=0) + event_time
        
        # Random event title
        event_title = random.choice(event_titles)
        
        events.append((event_datetime, event_title))
    
    # Sort events by date and time
    events.sort(key=lambda x: x[0])
    
    # Format the events
    formatted_events = [
        f"{event[0].strftime('%Y-%m-%d %H:%M')}: {event[1]}"
        for event in events
    ]
    print(f"Events: {formatted_events}")
    return formatted_events

list_calendar_events_tool = {
    "name": "list_calendar_events",
    "description": "Retrieves mock upcoming events from a simulated calendar",
    "parameter_definitions": {
        "days": {
            "description": "number of days to look ahead for events",
            "type": "int",
            "required": False,
            "default": 7
        },
        "max_results": {
            "description": "maximum number of events to retrieve",
            "type": "int",
            "required": False,
            "default": 10
        }
    }
}



import requests

def get_weather(city: str):
    print(f"Getting weather for {city}")
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    weather_data = response.json()
    print(f"Weather data: {weather_data['weather'][0]['avgtempF']}")
    return weather_data['weather'][0]['avgtempF']


list_weather_tool = {
  "name": "get_weather",
  "description": "returns the average temperature in Fahrenheit for the specified city",
  "parameter_definitions": {
    "city": {
      "description": "the name of the city to get weather for",
      "type": "str",
      "required": True
    }
  }
}


def get_wikipedia_content(title: str, sentences: int = 3):
    print(f"Getting wikipedia content for {title}")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Wikipedia content for {title}: {data['extract']}")
        return data['extract']
    else:
        return f"Error: Unable to retrieve content for '{title}'"

wikipedia_tool = {
    "name": "get_wikipedia_content",
    "description": "Retrieves the summary content of a Wikipedia page",
    "parameter_definitions": {
        "title": {
            "description": "the title of the Wikipedia page",
            "type": "str",
            "required": True
        },
        "sentences": {
            "description": "the number of sentences to retrieve from the summary",
            "type": "int",
            "required": False,
            "default": 3
        }
    }
}


from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5):
    print(f"Searching the web for {query}")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    print(f"Web search results for {query}: {results}")
    return [f"{result['title']}: {result['body']}" for result in results]

web_search_tool = {
    "name": "web_search",
    "description": "Performs a web search using DuckDuckGo and returns a list of search results",
    "parameter_definitions": {
        "query": {
            "description": "the search query string",
            "type": "str",
            "required": True
        },
        "max_results": {
            "description": "the maximum number of search results to return",
            "type": "int",
            "required": False,
            "default": 5
        }
    }
}



tools = [list_calendar_events_tool, list_weather_tool, wikipedia_tool, web_search_tool]

# helper function for routing to the correct tool
def invoke_tool(tool_call: cohere.ToolCall):
  if tool_call.name == list_calendar_events_tool["name"]:
    return [{
        "events": list_calendar_events()
    }]
  elif tool_call.name == list_weather_tool["name"]:
    city = tool_call.parameters["city"]
    return [{
        "weather": get_weather(city)
    }]
  elif tool_call.name == wikipedia_tool["name"]:
    title = tool_call.parameters["title"]
    return [{
        "content": get_wikipedia_content(title)
    }]
  elif tool_call.name == web_search_tool["name"]:
    query = tool_call.parameters["query"]
    return [{
        "results": web_search(query)
    }]
  else:
    raise f"Unknown tool name '{tool_call.name}'"
  

