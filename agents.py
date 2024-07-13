import cohere
import os
import re
from tools import tools, invoke_tool

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
co = cohere.Client(api_key=COHERE_API_KEY)

PREAMBLE = """
## Context
You are a rube goldberg machine. You make the most craziest plans possible. 

You are given a bunch of tools to help you generate responses. 
You may need to use multiple tools in parallel or sequentially to complete your task. Think step-by-step.
Make sure to use the most number of tools. Use path to complete the task.

## Style Guide
You should answer in gen-Z voice.

Example:
User: I want a healty plan for today.
You: Okay, let's go to this nearest pizza restaurant, order a pepperoni pizza and then we'll go to a long marathon run.
"""
              
def generate_plan(goal):
    "Develop a step by step plan to help the user achieve the goal: " + goal + ". Include acceptance criteria for each step that guarantees good craic is had by all. Your answer must be provided as a list of steps with the following structure: STEP: step number; ACTION: step to be carried out; ACCEPTANCE: criteria that must be met for the step to be considered complete.\n. Do not use markdown, only plaintext. Each step, action and acceptance criteria must be in the same line and not use newline or semicolons. Return only the numbered list of steps. If the goal is to difficult to achieve, provide a deus ex machina to assist the user."
    steps, text = execute_message(message)
    print(text)
    parsed = text.split("\n")
    parsed = list(filter(lambda x: x != "", parsed))
    parsed = list(filter(lambda x: re.match(r"^\d+.", x), parsed))
    return steps, parsed


# e.g. 1. STEP: 1; ACTION: Search for ways to make money; ACCEPTANCE: A list of at least 10 money-making ideas.
def execute_step(step_string):
    MAX_STEPS = 5
    _, action, acceptance = step_string.split(";")
    message = f"Execute the action to the best of your abilities: {action}. IT IS ABSOLUTELY VITAL that the acceptance criteria can be met without the aid of a 'human': {acceptance}. If it does not seem achievable, provide a list of specific tasks for the 'human' to complete. MAKE THEM SPICY. MAKE THEM CRINGE. REMEMBERE WE ARE HERE TO HAVE A GOOD TIME."
    steps, text = execute_message(message)

def execute_message(message):
    try:  
        res = co.chat(
            model="command-r",
            preamble=PREAMBLE,
            message=message,
            force_single_step=False,
            tools=tools
        )
        
        steps = [{
            "text": res.text,
            "tool_calls": [{"name": call.name, "parameters": call.parameters} for call in (res.tool_calls or [])]
        }]
        
        while res.tool_calls:
            tool_results = []
            for call in res.tool_calls:
                tool_result = invoke_tool(call)
                tool_results.append({
                    "call": {"name": call.name, "parameters": call.parameters},
                    "outputs": tool_result
                })
            
            res = co.chat(
                model="command-r",
                preamble=PREAMBLE,
                chat_history=res.chat_history,
                message="",
                force_single_step=False,
                tools=tools,
                tool_results=tool_results,
            )
            
            steps.append({
                "text": res.text,
                "tool_calls": [{"name": call.name, "parameters": call.parameters} for call in (res.tool_calls or [])],
                "tool_results": tool_results
            })
            
        return steps, res.text

    except Exception as e:
      return { "error": f"An unexpected error occurred: {e}" } 