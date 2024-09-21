
from textwrap import dedent
from .trip_task import TripTasks
from .trip_agent import TripAgents
from crewai import Crew

GITHUB_FUNCTION_CALLING_LLM="github/ai21-jamba-1.5-mini"
GROQ_FUNCTION_CALLING_LLM="groq/llama3-groq-70b-8192-tool-use-preview"
class TripCrew:

  def __init__(self, origin, cities, date_range, interests):
    self.cities = cities
    self.origin = origin
    self.interests = interests
    self.date_range = date_range

  def run(self):
    agents = TripAgents()
    tasks = TripTasks()

    city_selector_agent = agents.city_selection_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    identify_task = tasks.identify_task(
      city_selector_agent,
      self.origin,
      self.cities,
      self.interests,
      self.date_range
    )
    gather_task = tasks.gather_task(
      local_expert_agent,
      self.origin,
      self.interests,
      self.date_range
    )
    plan_task = tasks.plan_task(
      travel_concierge_agent, 
      self.origin,
      self.interests,
      self.date_range
    )

    crew = Crew(
      agents=[
        city_selector_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[identify_task, gather_task, plan_task],
      verbose=True,
    )

    result = crew.kickoff()
    return result


def run():
    location = "New York"
    cities = "Paris, London, Tokyo"
    date_range = "July 2022"
    interests = "Museums, Parks, Food"

    trip_crew = TripCrew(location, cities, date_range, interests)
    result = trip_crew.run()
    return result