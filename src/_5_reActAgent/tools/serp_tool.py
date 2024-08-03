from langchain.agents import Tool

from langchain_community.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()

serp_tool = Tool(
    name="serp_tool",
    description="A tool for searching the web for information.",
    func=search.run,
)