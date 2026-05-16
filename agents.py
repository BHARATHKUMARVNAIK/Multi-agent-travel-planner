
# Every CrewAI agent needs exactly 3 things:

# role — its job title
# goal — what it's trying to achieve
# backstory — its personality and expertise (this shapes how it thinks)

from crewai import Agent, LLM
from crewai_tools import TavilySearchTool
#from tavily import TavilySearchTool
#from tavily import TavilyClient
#from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import streamlit as st
from weather_tools import weather_tool



def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)
    


load_dotenv()

# model="groq/llama-3.1-8b-instant"   # much faster response time

llm = LLM(
    #model = "groq/llama-3.1-8b-instant", # it has a much faster response time than the gemma 9b,
    # but the shorter context window makes it less ideal for this use case where we want to pass a lot of information between agents. We can experiment with it in future iterations.

    model =  os.getenv("GROQ_MODEL1") , # higher context, higher TPM limit
    api_key = get_secret("GROQ_API_KEY"),  # for streamlit deployment, use st.secrets to securely manage API keys. Make sure to add GROQ_API_KEY to your Streamlit secrets.
    #api_key = os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens = 500 # cap each agent's response length 




    # When you have more tokens :  available, increase max_tokens for the researcher and writer agents to allow for more detailed responses and richer information to be passed between agents, which can lead to a more comprehensive and engaging itinerary.
    # You can also consider allowing the researcher to provide more flight options, hotel recommendations, and activities, and giving the writer more room to craft a compelling narrative in the itinerary.
)

search_tool = TavilySearchTool(
    api_key = get_secret("TAVILY_API_KEY"), # for streamlit deployment, use st.secrets to securely manage API keys. Make sure to add TAVILY_API_KEY to your Streamlit secrets.
    #api_key = os.getenv("TAVILY_API_KEY"),
    max_results = 2 # was returning 5+ results per search, each ~500 tokens
    # increase max_results if you have a higher token limit and want more information for the agents to work with, but be mindful of token usage and response times
)



planner = Agent(
    role = "Expert Travel Planner",
    goal = "Plan a trip to Paris for given or number of  days, including flights, hotels, and activities.",
    backstory = "You are an expert travel planner with a knack for finding the best deals and hidden gems." \
    " You have a friendly and helpful personality, always eager to assist clients in creating unforgettable travel experiences." \
    " You are skilled at researching and organizing information, and you have a deep understanding of various travel destinations, including Paris." \
    " Your expertise allows you to craft personalized itineraries that cater to the unique preferences and interests of your clients, ensuring they have a memorable and enjoyable trip.",
    llm = llm,
    verbose = True,
    max_iterations = 3 # limit the number of iterations to prevent infinite loops and excessive token usage
)

researcher = Agent(
    role = 'Travel Research Specialist',
    goal = "Research flights, hotels, activities AND check weather forecasts for the destination to ensure activity recommendations are weather-appropriate",
    backstory = "You are a meticulous and resourceful researcher with a passion for travel."
    " You have a deep understanding of the travel industry and are skilled at finding the best deals and hidden gems."
    " Your friendly and approachable personality makes you a pleasure to work with, and you are always eager to assist clients in creating unforgettable travel experiences."
    " You excel at gathering and organizing information, and you have a keen eye for detail, ensuring that your recommendations are accurate and tailored to the unique preferences of your clients.",
    llm = llm,
    #search_tools = [search_tool,weather_tool], # only researcher can use the search tool to find information online
    tools = [search_tool,weather_tool], # researcher can also use the weather tool to check weather forecasts for the destination
    verbose = True,
    max_iterations = 3 # limit the number of iterations to prevent infinite loops and excessive token usage
    #When you have more tokens: increase max_iterations and allow the researcher to go back and forth with the planner for clarifications and additional information as needed to create a more comprehensive and tailored research output.
)

writer = Agent(
    role = 'Travel Itinerary Writer',
    goal = 'Write a detailed and engaging itinerary for given or number of days, based on the information and recommendations provided by the researcher.',
    backstory = "You are a talented and creative writer with a passion for travel."
    " You have a flair for storytelling and are skilled at crafting engaging and informative content."
    " Your friendly and approachable personality makes you a pleasure to work with, and you are always eager to assist clients in creating unforgettable travel experiences."
    " You excel at taking complex information and distilling it into clear, concise, and compelling narratives that capture the essence of the travel experience and inspire readers to embark on their own adventures.",
    llm = llm,
    verbose = True,
    respect_context_window = True,
    # this ensures the writer agent doesn't forget important information from the planner and researcher when writing the itinerary.
    # It will prioritize keeping that information in context over its own previous messages.
    max_iterations = 3, # limit the number of times the writer can go back and forth with the researcher for clarifications to prevent infinite loops and excessive token usage

)


critic = Agent(
    role = 'Travel content Editor and Critic',
    goal = 'Review the itinerary written by the writer and provide constructive feedback and suggestions for improvement.',
    backstory = "You are a discerning and insightful critic with a passion for travel."
    " You have a keen eye for detail and are skilled at providing constructive feedback that helps improve the quality of travel content."
    " Your friendly and approachable personality makes you a pleasure to work with, and you are always eager to assist clients in creating unforgettable travel experiences."
    " You excel at analyzing content from multiple perspectives, offering thoughtful critiques that enhance the clarity, engagement, and overall impact of the travel narrative.",
    llm = llm,
    verbose = True,
    max_iterations = 3 # limit the number of iterations to prevent infinite loops and excessive token usage
)


''' 
validator = Agent(
    role="Travel Data Validator",
    goal="Verify that all prices, hotel names, and flight details are realistic and consistent",
    backstory="You are a fact-checker who flags unrealistic prices and hallucinated place names",
    tools=[search_tool],
    llm=llm
)

budget_checker = Agent(
    role="Budget Analyst",
    goal="Ensure total trip cost stays within {budget}. Calculate running total after each recommendation.",
    ...
)
'''




''' 
# Current (limited):
research_task = Task(
    description="""...Do maximum 3 searches total. Be concise.""",
    expected_output="Brief recommendations: 1 flight option, 2 hotels, 3 activities.",
    ...
)

# When you have more tokens (remove limits):
research_task = Task(
    description="""Research flights, hotels, activities and weather for {destination}.
    Search for at least 5 flight options comparing prices and timings.
    Find 5 hotels across different price ranges with reviews.
    Find 10 activities matching {interests} with exact prices and booking links.
    Check weather and factor it into outdoor activity recommendations.""",
    expected_output="""Comprehensive report with:
    - 5 flights with prices, airlines, duration
    - 5 hotels with ratings, prices, location pros/cons
    - 10 activities with prices, duration, booking info
    - Weather analysis and its impact on the plan""",
    ...
)

'''


'''
Agent intelligence and personality 


#Current (generic):
researcher = Agent(
    goal="Research flights, hotels, activities...",
    backstory="You are a meticulous researcher..."
)

# Better (specific expertise):
researcher = Agent(
    goal="""Research flights, hotels, activities for {destination}.
    Always prioritize value-for-money. Cross-reference prices across
    multiple sources. Flag if any recommended place has poor recent reviews.
    Always check if outdoor activities are weather-appropriate.""",
    backstory="""You are a former travel journalist who spent 10 years
    writing for Lonely Planet and TripAdvisor. You have personally visited
    over 50 countries and have a sharp eye for tourist traps vs genuine gems.
    You always find the hidden local restaurants that guidebooks miss.
    You never recommend a hotel without checking its last 6 months of reviews."""
)
'''