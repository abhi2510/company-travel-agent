import time

from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenRouter(model=os.getenv('OPENROUTER_MODEL_NAME'))

def llm_invoke(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            print(f"LLM attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    