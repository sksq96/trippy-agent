from flask import Flask, request, jsonify
import cohere
import os
from tools import tools, invoke_tool

app = Flask(__name__)

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

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    goal = data.get('goal')
    location = data.get('location')
    
    if not goal:
        return jsonify({"error": "No goal provided"}), 400
    
    message = goal
    if location:
        message += f" (Location: {location['lat']}, {location['lon']})"
    
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
        
        return jsonify({"plan": steps})
    
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)