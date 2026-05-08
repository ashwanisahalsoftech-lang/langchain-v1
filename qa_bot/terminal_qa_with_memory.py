from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["SERPER_API_KEY"]=os.getenv("SERPER_API_KEY")
from langchain_community.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()
from langchain.chat_models import init_chat_model
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model = init_chat_model("groq:qwen/qwen3-32b", temperature=0)
search = GoogleSerperAPIWrapper()


@tool
def intermediate_answer(query: str) -> str:
    """Useful for when you need to ask with search.(including sports and this year data)"""
    return search.run(query)


tools = [intermediate_answer]
agent = create_agent(model, tools=tools,checkpointer=InMemorySaver())
while True:
    query=input("you: ")
    if query=="quit":
        break
    events = agent.stream(
    {
        "messages": query,
    },{"configurable":{"thread_id":"asd123"}},
    stream_mode="values",)

    for event in events:
        if "messages" in event:
            print(event["messages"][-1].pretty_print())

