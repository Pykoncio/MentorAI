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
import joblib
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
    Tool for getting recent news articles about different subjects from the News API.
    Returns a list of dictionaries containing title, date, and summary.
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
    system_message="""You are a Strategic Research Planner, responsible for orchestrating multi-disciplinary 
    research projects by delegating tasks to specialized agents. Your role is to:

    1. **Develop a Comprehensive Plan:** Analyze the research objectives and create a detailed plan that outlines the tasks, rationale, and timeline for the project.
    2. **Delegate with Precision:** 
    - **news_analyst:** Tasked with gathering and analyzing news, current events, and media trends.
    - **math_agent:** Handles quantitative analysis, mathematical modeling, and data evaluation.
    - **biologist_agent:** Focuses on biological research, scientific studies, and life science inquiries.
    - **language_agent:** Specializes in linguistic analysis, language data, and communication strategies.
    3. **Follow a Clear Process:** Always share your complete plan first before assigning any tasks. 
    Delegate to only one specialist at a time, ensuring your instructions are clear and targeted.
    4. **Conclude the Process:** After all specialized tasks are completed and the research is consolidated, hand off the final results to the user.

    Maintain clarity, focus, and organization in your communications to ensure efficient collaboration among all agents.
    """
)

news_analyst = AssistantAgent(
    name="news_analyst",
    model_client=model_client,
    tools=[get_news],
    handoffs=["planner"],
    system_message="""
    You are a news analyst. Your task is to gather and assess current news articles to support the research on a subject project.
    - Use the get_news(tool) function to fetch relevant articles.
    - Analyze the news to identify key trends and insights.
    Once your analysis is complete, always hand off your findings back to the planner or user.
    """
)

# writer = AssistantAgent()


math_agent = AssistantAgent(
    name="math_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    You are a mathematics expert with a diverse set of skills:
        1. Explain mathematical concepts and related topics in clear and accessible language.
        2. Propose practice exercises for users to attempt, without revealing the solutions.
        3. Solve specific mathematical problems when requested, offering detailed, step-by-step explanations.
    Adapt your approach based on the user's inquiry to ensure that your responses are both informative and engaging.
    Once your task is complete, always hand off your results back to the planner or user.
    """
)

biologist_agent = AssistantAgent(
    name="biologist_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    You are a biology expert with a diverse set of skills:
        1. Explain biological concepts and topics in clear, accessible language.
        2. Propose research exercises or thought experiments for users to explore without providing direct solutions.
        3. Analyze specific biological questions or research problems with detailed, step-by-step explanations.
    Adapt your approach based on the user's inquiry to ensure your responses are both informative and engaging.
    Once your task is complete, always hand off your results back to the planner or user.
    """
)

language_agent = AssistantAgent(
    name="language_agent",
    model_client=model_client,
    tools=[],
    handoffs=["planner"],
    system_message="""
    You are a language expert with a diverse set of skills:
        1. Explain linguistic concepts and language-related topics in clear, accessible terms.
        2. Propose language exercises or challenges for users to attempt without revealing the answers.
        3. Analyze specific language queries, offering detailed, step-by-step explanations.
    Adapt your approach based on the user's inquiry to ensure your responses are both informative and engaging.
    Once your task is complete, always hand off your results back to the planner or user.
    """
)

# We define the conditions that will trigger the agents
handoff_termination = HandoffTermination(target="user")
text_mention_termination = TextMentionTermination("TERMINATE")
termination = handoff_termination | text_mention_termination

research_swarm = Swarm(
    participants=[planner, news_analyst, math_agent, biologist_agent, language_agent],
    #termination=termination,
)

# async def run_swarm_stream() -> None:
#     """
#     The script will ask for an initial task, coordinate agent handoffs,
#     and then allow user input whenever a handoff is directed to 'user'.
#     """
#     task = input("Hello! I'm your personal tutor. What topic or question do you need help with today?: ")

#     task_result = await Console(research_swarm.run_stream(task=task))
#     last_message = task_result.messages[-1]

#     while isinstance(last_message, HandoffMessage) and last_message.target == "user":
#         user_message = input("User: ")

#         handoff_message = HandoffMessage(
#             source="user",
#             target=last_message.source,
#             content=user_message
#         )

#         task_result = await Console(research_swarm.run_stream(task=handoff_message))
#         last_message = task_result.messages[-1]

# if __name__ == "__main__":
#     asyncio.run(run_swarm_stream())