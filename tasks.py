
# Every CrewAI Task needs:

# description — exact instructions for what to do
# expected_output — what the final result should look like
# agent — which agent does this task

from crewai import Task
from agents import planner, researcher, writer , critic


# description="___",        # What should the planner do?
# expected_output="___",    # What does a good plan look like?
# agent=planner

''' 

plan_task = Task(
    description = "Plan a trip {departure} to {destination} for {num_days} days, with a budget of {budget} and travel style of {travel_style}, main places of interest {interests} including flights, hotels, and activities.",
    expected_output = "A detailed travel plan from {departure} to {destination} for {num_days} days,with a budget of {budget} and travel style of {travel_style}, main places of interest {interests} including flights, hotels, and activities.",
    agent = planner
)

research_task = Task(
    description = "Research the best flights, hotels, and activities in {destination} for {num_days} days,with a budget of {budget} and travel style of {travel_style}, main places of interest {interests} and provide detailed information and recommendations to the planner.",
    expected_output = "Detailed information and recommendations for the best flights, hotels, and activities in {destination} for {num_days} days,with a budget of {budget} and travel style of {travel_style}, main places of interest {interests} to assist the planner in creating a comprehensive travel plan.",        
    agent = researcher
)

writer_task = Task(
    description = "Write a detailed and engaging itinerary for {num_days} days, based on the information and recommendations provided by the researcher.",
    expected_output = "A detailed and engaging itinerary for a trip to {destination} for {num_days} days, with a budget of {budget} and travel style of {travel_style}, main places of interest {interests} including flights, hotels, and activities.",
    agent = writer
)

critique_task = Task(
    description = "Critique the itinerary written by the writer, and provide feedback and suggestions for improvement to the writer.",
    expected_output = "Constructive feedback and suggestions for improvement for the itinerary written by the writer.",
    agent = critic
)

'''

plan_task = Task(
    description="Plan a {num_days}-day trip from {departure} to {destination}. Budget: {budget}. Style: {travel_style}. Interests: {interests}.",
    expected_output="A concise {num_days}-day travel outline with flights, hotels, activities.",
    agent=planner
)

''' 
research_task = Task(
    description="Research flights, hotels, activities and weather for {destination}, {num_days} days. Budget: {budget}. Style: {travel_style}. Interests: {interests}.",
    expected_output="Key recommendations for flights, 2-3 hotels, top activities with prices.",
    agent=researcher
)
'''
research_task = Task(
    description="""Research for {destination}, {num_days} days. 
    Budget: {budget}. Style: {travel_style}. Interests: {interests}.
    Do maximum 3 searches total. Be concise.""",
    expected_output="Brief recommendations: 1 flight option, 2 hotels, 3 activities with prices.",
    agent=researcher
)


writer_task = Task(
    description="Write a {num_days}-day itinerary for {destination} using the researcher's findings. Style: {travel_style}.",
    expected_output="A day-by-day itinerary with morning, afternoon, evening plans.",
    agent=writer
)

critique_task = Task(
    description="Review the itinerary for completeness and accuracy. Flag any issues.",
    expected_output="Brief feedback and an improved final itinerary.",
    agent=critic
)

