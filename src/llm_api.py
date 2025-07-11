
import requests
import json

def mcp_request(api_url, 
                api_key, 
                model_name, 
                mcp_url, 
                mcp_tool_name, 
                mcp_tool_description, 
                mcp_property_name, 
                mcp_property_description, 
                llm_prompt):

    """ 
    boilerplate taken from: 
    https://apidog.com/blog/use-mcp-servers-with-openrouter/
    
    executes a chat completion request with mcp tool use 

    """

    headers = {"Authorization": "Bearer "+api_key, "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": llm_prompt}],
        "tools": [{
            "type": "function",
            "function": {
                "name": mcp_tool_name,
                "description": mcp_tool_description,
                "parameters": {
                    "type": "object",
                    "properties": {mcp_property_name: {"type": "string", "description": mcp_property_description}},
                    "required": [mcp_property_name]
                }
            }
        }]
    }

    response = requests.post(api_url, headers=headers, json=payload)
    message = response.json()["choices"][0]["message"]

    if "tool_calls" in message:
        tool_call = message["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        mcp_response = requests.post(mcp_url, json={"name": function_name, "arguments": arguments})
        tool_result = mcp_response.json()["result"]
        
        messages = payload["messages"] + [
            {"role": "assistant", "content": null, "tool_calls": [tool_call]},
            {"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(tool_result)}
        ]
        
        final_response = requests.post(api_url, headers=headers, json={"model": "openai/gpt-4", "messages": messages})
        
        return final_response.json()["choices"][0]["message"]["content"]
    


