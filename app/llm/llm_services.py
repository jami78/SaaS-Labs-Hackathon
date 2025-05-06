from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

llm_openai= ChatOpenAI(model='gpt-4o', temperature=0.2)