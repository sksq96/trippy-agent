from flask import Flask, request, jsonify
import cohere
import os
from tools import tools, invoke_tool

app = Flask(__name__)

COHERE_API_KEY = "tBZEDWJ0DN7QIWxNrz525ZiW8rnU2JMT2Zvv5pNv"
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

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    goal = data.get('goal')
    
    if not goal:
        return jsonify({"error": "No goal provided"}), 400
    
    res = co.chat(
        model="command-r",
        preamble=PREAMBLE,
        message=goal,
        force_single_step=False,
        tools=tools
    )
    
    steps = [res.text]
    
    while res.tool_calls:
        tool_results = []
        for call in res.tool_calls:
            tool_results.append({"call": call, "outputs": invoke_tool(call)})
        
        res = co.chat(
            model="command-r",
            preamble=PREAMBLE,
            chat_history=res.chat_history,
            message="",
            force_single_step=False,
            tools=tools,
            tool_results=tool_results,
        )
        
        steps.append(res.text)
    
    return jsonify({"plan": steps})

if __name__ == '__main__':
    app.run(debug=True)
