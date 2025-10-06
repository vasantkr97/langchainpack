import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
#Creating example prompt template
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])
#few shot prompt creation
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

#create the final prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analysis assistant. Classify the sentiment as Positive, Negative, or Neutral."),
    few_shot_prompt,
    ("human", "{input}")
])

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

pipeline = final_prompt | llm

test_input = "This restaurant has wrost food but the service could be better."
res = pipeline.invoke({"input": test_input})

print(res.content)