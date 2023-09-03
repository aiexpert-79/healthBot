import openai
import gradio as gr
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

pdf_path = "docs"
def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text
print("pdf")

def construct_index(directory_path):
    max_input_size = 4096
    max_tokens = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, max_tokens, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo", max_tokens=max_tokens))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex(documents=documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=3, label="Enter your text"),
                     outputs="text",
                     title="Arabic Assistor")

index = construct_index("docs")
iface.launch(share=True)