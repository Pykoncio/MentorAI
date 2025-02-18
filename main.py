from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio
import os
from typing import Any, Dict, List
from datetime import datetime

from dotenv import load_dotenv
import aiohttp

# Load environment variables from .env
load_dotenv()

# Get API keys from environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("The NEWS_API_KEY is not found. Ensure it is set in your .env file.")

# We define the functions (tools) that will be used by the agents
async def get_news(query: str) -> List[Dict[str, str]]:
    """
    
    """
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5 
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            data = await response.json()

    articles = data.get("articles", [])
    news_data = []
    for article in articles:
        news_data.append({
            "title": article.get("title", "No Title"),
            "date": article.get("publishedAt", "Unknown Date"),
            "summary": article.get("description", "No Description Provided")
        })

    return news_data

# async def write_report(content: str, agent_name: str) -> Dict[str, str]:
#     return {"file_path": file_path}

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
)

# We define now the different agents
planner = AssistantAgent(
    name="planner",
    model_client=model_client,
    handoffs=["news_analyst", "math_agent", "biologist_agent", "language_agent", "user"],
    system_message="""

    """
)

news_analyst = AssistantAgent(
    name="news_analyst",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    """
)

# writer = AssistantAgent()


math_agent = AssistantAgent(
    name="math_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    """
)

biologist_agent = AssistantAgent(
    name="biologist_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    """
)

language_agent = AssistantAgent(
    name="language_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    """
)

# We define the conditions that will trigger the agents
handoff_termination = HandoffTermination(target="user")
text_mention_termination = TextMentionTermination()
termination = handoff_termination | text_mention_termination

research_swarm = Swarm(
    participants=[planner, news_analyst, math_agent, biologist_agent, language_agent],
    termination=termination,
)

async def run_swarm_stream() -> None:
    """
    """
    task = input("Please enter the initial task: ")

    # Start the multi-agent conversation with the provided task
    task_result = await Console(research_swarm.run_stream(task=task))
    last_message = task_result.messages[-1]

    # Continue looping if the last message is a Handoff to the user
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")

        # Create a new HandoffMessage that sends the user's reply
        # back to whoever delegated (last_message.source)
        handoff_message = HandoffMessage(
            source="user",
            target=last_message.source,
            content=user_message
        )

        task_result = await Console(research_swarm.run_stream(task=handoff_message))
        last_message = task_result.messages[-1]

if __name__ == "__main__":
    asyncio.run(run_swarm_stream())