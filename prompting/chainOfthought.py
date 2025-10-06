import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai_model = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0.0, model=openai_model)

#defining the chain of though prompt template (system prompt)
cot_system_prompt = """
Be a helpful assistant and answer the user's question.

To answer the question, you must:

- List systematically and in precise detail all
  subproblems that need to be solved to answer the
  question.
- Solve each sub problem INDIVIDUALLY and in sequence.
- Finally, use everything you have worked through to
  provide the final answer.
"""
#define normal math query
query="How many keyshrokes are needed to type the numbers from 1 to 500?"
 
cot_prompt_template = ChatPromptTemplate.from_messages([
    ("system", cot_system_prompt),
    ("human", "{query}")
])

cot_pipeline = cot_prompt_template | llm

cot_result = cot_pipeline.invoke({"query": query})
console.print(Markdown(cot_result.content))















# no_cot_system_prompt = """
# Be a helpful assistant and answer the user's question.

# You MUST answer the question directly without any other
# text or explanation.
# """

# no_cot_prompt_template = ChatPromptTemplate.from_messages([
#     ("system", no_cot_system_prompt),
#     ("user", "{query}")
# ])

# query = (
#     "How many keyshrokes are needed to type the numbers from 1 to 500?"
# )

# #pipeline 
# no_cot_pipeline = no_cot_prompt_template | llm

# no_cot_result = no_cot_pipeline.invoke({"query": query}).content
# print(no_cot_result)