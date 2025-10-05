import os
from dotenv import load_dotenv
from langsmith import traceable
import random
import time
from tqdm.auto import tqdm

# Load environment variables first
load_dotenv()

# Set LangSmith configuration
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "aurelioai-langchain-course-langsmith-openai"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Import after environment is configured
from langchain_openai import ChatOpenAI

# Get API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize the model
llm = ChatOpenAI(
    temperature=0.0, 
    model="gpt-4o-mini",
    openai_api_key=openai_api_key
)

# Invoke the model
response = llm.invoke("hello")

@traceable
def generate_random_number(): 
    return random.randint(0, 100)

@traceable
def generate_string_delay(input_str: str):
    number = random.randint(1,5)
    time.sleep(number)
    return f"{input_str} ({number})"

@traceable
def random_error():
    number = random.randint(0,1)
    if number == 0:
        raise ValueError("Random error")
    else:
        return "No error"
    
generate_random_number()
generate_string_delay("vasanth")
random_error()


@traceable(name="Chitchat Maker")
def error_generation_function(question: str): 
    delay = random.randint(0,3)
    time.sleep(delay)
    number = random.randint(0,1)
    if number == 0:
        raise ValueError("Random error")
    else:
        return "Im great how are you?"


@traceable(name="Safe Error Handler")
def safe_call():
    try: 
        return error_generation_function("How are you today?")
    except ValueError:
        return "Recovered from error"


for _ in tqdm(range(10)):
    safe_call()

