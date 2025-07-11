import asyncio
from fastmcp import Client

# Local Python script
client = Client("./src/debug.py")


async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()

        print(tools)

        # Execute operations
        result = await client.call_tool(
            "debug_crash", {"target": "occasional-cpp.exe", "args": []}
        )
        print(result.content)


asyncio.run(main())
