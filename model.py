from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()


def getModel():
 return OllamaLLM(model="mistral")
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         google_api_key=os.getenv("GEMINI_API_KEY"),
#         temperature=0.3,
#     )