import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") 

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "aurelioai-langchain-course-chat-memory-openai"

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", api_key=openai_api_key)

system_prompt = "You area beautiful helpful assistant called Zeta"

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{query}")
])

chat_map = {}
def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_map:
        chat_map[session_id] = InMemoryChatMessageHistory()
    return chat_map[session_id]


pipeline = prompt_template | llm

pipeline_with_history = RunnableWithMessageHistory(
    pipeline,
    get_session_history=get_chat_history,
    input_messages_key="query",
    history_messages_key="history"
)

res = pipeline_with_history.invoke(
    {"query": "Hi, my name is vasanth"},
    config={"session_id": "id_123"}
)

print(res)

res = pipeline_with_history.invoke(
    {"query": "what is my name again?"},
    config={"session_id": "id_123"}
)

print(res)





















# memory = ConversationBufferMemory(return_messages=True)

# memory.save_context(
#     {"input": "Hi, my name is James"},  # user message
#     {"output": "Hey James, what's up? I'm an AI model called Zeta."}  # AI response
# )
# memory.save_context(
#     {"input": "I'm researching the different types of conversational memory."},  # user message
#     {"output": "That's interesting, what are some examples?"}  # AI response
# )
# memory.save_context(
#     {"input": "I've been looking at ConversationBufferMemory and ConversationBufferWindowMemory."},  # user message
#     {"output": "That's interesting, what's the difference?"}  # AI response
# )
# memory.save_context(
#     {"input": "Buffer memory just stores the entire conversation, right?"},  # user message
#     {"output": "That makes sense, what about ConversationBufferWindowMemory?"}  # AI response
# )
# memory.save_context(
#     {"input": "Buffer window memory stores the last k messages, dropping the rest."},  # user message
#     {"output": "Very cool!"}  # AI response
# )


# response = memory.load_memory_variables({})

# # print(response)

# chain = ConversationChain(
#     llm=llm,
#     memory=memory,
#     verbose=True
# )

# res = chain.invoke({"input": "what is my name again?"})

# print(res)