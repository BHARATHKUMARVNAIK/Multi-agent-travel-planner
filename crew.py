
# The Manager

# This file just assembles the team and runs them in order
# CrewAI's Crew needs : 

# agents — list of all your agents
# tasks — list of all tasks in the order they should run
# process — how they work together (Process.sequential means one after another, which is what we want)

from crewai import Crew, Process
from agents import planner, researcher, writer, critic
from tasks import plan_task, research_task, writer_task, critique_task
import time


def task_callback(output):
    print("Task completed , sleeping 30s to reset token limit before next task starts...")
    time.sleep(30) # pause between each task.

# The crew object — just the team setup
crew = Crew(
    agents = [
        planner,
        researcher,
        writer,
        critic
    ],
    tasks = [
        plan_task,
        research_task,
        writer_task,
        critique_task
    ],
    process = Process.sequential,
    verbose = False, # 👈 stops printing every agent thought to terminal
    task_callback=task_callback, # 👈 callback function to pause between tasks
    memory = False # keeps all previous task outputs in context for the agents to refer back to and build on as they work through the tasks
)

# The function the UI will call
def run_crew(departure, destination,num_days,budget,travel_style,interests):
    #time.sleep(60) #wait 60s so token limit resets before writer starts
    result = crew.kickoff(inputs={
        "departure" : departure,
        "destination" : destination,
        "num_days" : num_days,
        "budget" : budget,
        "travel_style" : travel_style,
        "interests" : interests
    })
    return result

