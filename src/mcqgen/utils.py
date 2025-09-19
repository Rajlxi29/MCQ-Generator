import os
import traceback
import PyPDF2
import json
import re


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )
    

def get_table_data(quiz_str):
    try:
        if isinstance(quiz_str, dict):
            quiz_dict = quiz_str
        elif isinstance(quiz_str, str):
            quiz_str = quiz_str.strip()

            if quiz_str.startswith("```"):
                quiz_str = re.sub(r"^```(json)?", "", quiz_str)
                quiz_str = quiz_str.strip("`").strip()

            start = quiz_str.find("{")
            end = quiz_str.rfind("}")
            if start != -1 and end != -1:
                quiz_str = quiz_str[start:end+1]

            quiz_dict = json.loads(quiz_str)
        else:
            raise ValueError("Quiz input must be a JSON string or dictionary")

        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = "\n".join(
                [f"{opt}-> {opt_val}" for opt, opt_val in value.get("options", {}).items()]
            )
            correct = value.get("correct", "")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
