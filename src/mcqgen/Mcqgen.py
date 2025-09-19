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
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

quiz_template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=quiz_template
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz", verbose=True)

evaluate_template="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:"""

evaluate_prompt = PromptTemplate(
    input_variables = ["subject", "quiz"],
    template = evaluate_template
)

eval_chain = LLMChain(llm=llm, prompt=evaluate_prompt, output_key="review", verbose=True)

final_mcq_generator = SequentialChain(chains=[quiz_chain, eval_chain],
                                      input_variables = ["text", "number", "subject", "tone", "response_json"],
                                      output_variables = ["quiz", "review"], verbose = True)

