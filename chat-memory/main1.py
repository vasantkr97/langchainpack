import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.runnables import ConfigurableFieldSpec, RunnableWithMessageHistory
from pydantic import BaseModel, Field

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") 

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "aurelioai-langchain-course-chat-memory-openai"


open_api_key = os.getenv("OPENAPI_API_KEY")
llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini",api_key=open_api_key)

system_prompt = "You are a helpful assistant called Zeta."

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{query}")
])

pipeline = prompt_template | llm

class BufferWindowMessageHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    k: int = Field(default_factory=int)

    def __init__(self, k: int):
        super().__init__(k=k)
        print(f"Initialiazing BufferWindowMessageHistory with k={k}")
    
    def add_messages(self, messages: list[BaseMessage]) -> None:
        """Add messages to the messages to the history, removing any messages beyond the last k messages."""
        self.messages.extend(messages)
        self.messages = self.messages[-self.k:]
    
    def clear(self) -> None:
        "Clear the history"
        self.messages = []


chat_map = {}

def get_chat_history(session_id: str, k: int=10) -> BufferWindowMessageHistory:
    print(f"get_chat_history called with session_id={session_id} and k={k}")

    if session_id not in chat_map:
        chat_map[session_id] = BufferWindowMessageHistory(k=k)
    return chat_map[session_id]


pipeline_with_history = RunnableWithMessageHistory(
    pipeline,
    get_session_history=get_chat_history,
    input_messages_key="query",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="session_id",
            annotation=str,
            name="Session ID",
            description="The session ID to use for the chat history",
            default="id_default",
        ),
        ConfigurableFieldSpec(
            id="k",
            annotation=int,
            name="k",
            description="The number of messages to keep in the history",
            default=10,
        )
    ]
)

res = pipeline_with_history.invoke(
    {"query": "hi, my name is vasanth"},
    config={"configurable": {"session_id": "id_k4", "k":10}}
)

print(res.content)

res = pipeline_with_history.invoke(
    {"query": "what is my name again?"},
    config={"configurable": {"session_id": "id_k4", "k": 4}}
)

print(res.content)