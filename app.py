import sys
import os
import reportlab
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import streamlit as st
import traceback
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgen.utils import get_table_data, read_file, create_pdf
from src.mcqgen.logger import logging
from src.mcqgen.Mcqgen import final_mcq_generator

with open(r"D:\GenAI\MCQ Generator\response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

#Streamlit

st.title("MCQ Generator")

with st.form("input data"):
    text_file = st.file_uploader("Get the file")

    number = st.number_input("Number of MCQ", min_value=5, max_value=50)

    subject = st.text_input("what to extract", max_chars=30)

    tone = st.text_input("Difficulty level", max_chars = 10, placeholder="Simple")

    button = st.form_submit_button("click to submit the form")


if button and text_file is not None and subject and tone and number:
    try:
        with st.spinner("generating..."):
            text = text_file.read().decode("utf-8")

            with get_openai_callback() as cb:
                response = final_mcq_generator(
                    {
                    "text":text,
                    "number":number,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(RESPONSE_JSON)
                    }
                )
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        st.error("Error")
        
    else:
        if isinstance(response,dict):
            quiz = response.get("quiz",None)
            if quiz is not None :
                table = get_table_data(quiz)
                if not table:
                    st.error("table cannot be generated")
                else:                     
                    df = pd.DataFrame(table)

                    df.index = df.index+1
                    for idx, row in df.iterrows():
                        st.markdown(f"**Q{idx}: {row['MCQ']}**")
                        st.text(row['Choices'])   
                        st.markdown(f"**Correct Answer:** {row['Correct']}")
                        st.markdown("---")

                        
                    pdf_buffer = create_pdf(df)

                    st.download_button(
                        label="Download MCQs as PDF",
                        data=pdf_buffer.getvalue(),
                        file_name="generated_mcqs.pdf",
                        mime="application/pdf"
                    )

                    st.text_area(label="Review", value=response["review"])
                        
            else:
                st.error("No quiz data in response")

        else:
            st.write("Raw Response:",response)


    

    