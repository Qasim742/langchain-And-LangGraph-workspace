import os 
from typing import Annotated, TypedDict 
from langchain_core.messages import BaseMessage, HumanMessage 
from langchain_groq import ChatGroq 
from langgraph.graph import END, START, StateGraph 
from langgraph.graph.message import add_messages 
from langgraph.checkpoint.memory import MemorySaver
import dotenv
dotenv.load_dotenv()


class ChatState(TypedDict): 
   # 'add_messages' ensures state appends messages rather than replacing them 
   messages: Annotated[list[BaseMessage], add_messages]


   # load api key from .env file
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=api_key)



def chat_node(state: ChatState): 
   # Extract current conversation messages 
   messages = state["messages"] 
    
   # Invoke Grok API model 
   response = llm.invoke(messages) 
    
   # Return response in a list to merge via add_messages reducer 
   return {"messages": [response]}


# Create graph instance 
graph = StateGraph(ChatState) 
 
# Add chat node 
graph.add_node("chat_node", chat_node) 
 
# Set edges 
graph.add_edge(START, "chat_node") 
graph.add_edge("chat_node", END) 
 
# Add Memory Saver Checkpointer for conversation persistence 
checkpointer = MemorySaver() 
 
# Compile the graph with checkpointer 
chatbot = graph.compile(checkpointer=checkpointer) 
