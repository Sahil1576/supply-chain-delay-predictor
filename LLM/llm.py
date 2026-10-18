from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(model="ministral-8b-latest")