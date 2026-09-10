from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenRouter(model=os.getenv('OPENROUTER_MODEL_NAME'))