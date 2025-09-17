import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pandas as pd 
import traceback
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgen.utils import get_table_data, read_file
from src.mcqgen.logger import logging
import PyPDF2
import re

load_dotenv()

llm = ChatOpenAI(
    model =  "deepseek/deepseek-chat-v3.1:free",
    temperature = 0.8,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)