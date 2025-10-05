dependencies = [
    "langchain-community==0.3.16",
    "langchain-core==0.3.33",
    "langchain-openai==0.3.3",
    "langsmith==0.3.4",
    "python-dotenv>=1.1.1",
]



dependencies = [
    "langchain>=0.3.0",              # ← ADDED: Main langchain package
    "langchain-community>=0.3.0",    # ← Changed from ==0.3.16 to >=0.3.0
    "langchain-core>=0.3.0",         # ← Changed from ==0.3.33 to >=0.3.0
    "langchain-openai>=0.2.0",       # ← Changed from ==0.3.3 to >=0.2.0
    "langsmith>=0.3.0",              # ← Changed from ==0.3.4 to >=0.3.0
    "python-dotenv>=1.1.1",
    "pydantic>=2.0.0,<3.0.0",        # ← ADDED: Explicit pydantic version
    "pydantic-core>=2.0.0",          # ← ADDED: Pydantic core dependency
]