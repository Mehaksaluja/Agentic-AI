from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from config import Config
from tools.weather_tool import get_weather


class WeatherAgent:
    def __init__(self):
        llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.MODEL_NAME,
            temperature=0,
        )
        self.graph = create_react_agent(llm, [get_weather])

    def ask(self, question: str) -> str:
        result = self.graph.invoke(
            {"messages": [("user", question)]}
        )
        return result["messages"][-1].content
