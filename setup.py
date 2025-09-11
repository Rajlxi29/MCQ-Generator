from setuptools import find_packages, setup

setup(
    name='MCQ Generator',
    version='0.0.1',
    author='Nilesh Raj',
    authoremail='nileshraji811001@gmail.com',
    install_requires=["openai", "streamlit", "langchain", "PyPDF2", "python-dotenv"],
    packages=find_packages()
)