import Streamlitapp as st
import traceback
import json
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgen.utils import get_table_data, read_file
from src.mcqgen.logger import logging
from src.mcqgen.Mcqgen import final_mcq_generator