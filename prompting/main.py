
import os
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") or \
    getpass("Enter LangSmith API Key: ")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "aurelioai-langchain-course-prompts-openai"



prompt = """
Answer the user's query based on the context below.
If you cannot answer the question using the
provided information answer with "I don't know".

Context: {context}
"""

from langchain.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate
# from rich.console import Console
# from rich.markdown import Markdown

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model = "gpt-4o-mini"

llm = ChatOpenAI(temperature=0.0, model=openai_model)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ('user', "{query}"),
])

# print(prompt_template.input_variables)

# print(prompt_template.messages)

from langchain.prompts import ( 
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(prompt),
    HumanMessagePromptTemplate.from_template("{query}"),
])

# print(prompt_template.messages)

pipeline = (
    {
        "query": lambda x: x["query"],
        "context": lambda x: x["context"]
    }
    | prompt_template
    | llm
)

context = """Aurelio AI is an AI company developing tooling for AI
engineers. Their focus is on language AI with the team having strong
expertise in building AI agents and a strong background in
information retrieval.

The company is behind several open source frameworks, most notably
Semantic Router and Semantic Chunkers. They also have an AI
Platform providing engineers with tooling to help them build with
AI. Finally, the team also provides development services to other
organizations to help them bring their AI tech to market.

Aurelio AI became LangChain Experts in September 2024 after a long
track record of delivering AI solutions built with the LangChain
ecosystem."""

query = "what does Aurelio AI do?"

res = pipeline.invoke({ "query": query, "context": context})
# print("ia generated",res.content)
                            

#few shot prompting 

#creating templete for prompt
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])


# Define the examples
examples = [
    {
        "input": "I absolutely loved this movie! It was amazing!",
        "output": "Positive"
    },
    {
        "input": "This product is terrible. Complete waste of money.",
        "output": "Negative"
    },
    {
        "input": "The weather is okay today, nothing special.",
        "output": "Neutral"
    }
]

#create few shot prompt 
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# print(few_shot_prompt.format())


new_system_prompt = """
Answer the user's query based on the context below.
If you cannot answer the question using the
provided information answer with "I don't know".

Always answer in markdown format. When doing so please
provide headers, short summaries, follow with bullet
points, then conclude.

Context: {context}
"""


res = pipeline.invoke({ "query": query, "context": context })

# console = Console()

# console.print(Markdown(res.content))

#final prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analysis assistant. Classify the sentiment as Positive, Negative, or Neutral."),
    few_shot_prompt,
    ("human", "{input}")
])

pipelineChain = final_prompt | llm

test_input = "This restaurant has worst food but the service could be better"

result = pipelineChain.invoke({"input": test_input})

# print(result.content)



