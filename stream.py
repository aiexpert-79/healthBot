import openai
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Replace with your OpenAI API key

def stream_chat(conversation):
    response = openai.Completion.create(
        engine="text-davinci-003",
        messages=conversation,
        stop=None
    )
    return response.choices[0].message

def main():
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    def chat(input_text):
        conversation.append({"role": "user", "content": input_text})
        response = stream_chat(conversation)
        conversation.append({"role": "assistant", "content": response["content"]})
        return response["content"]

    iface = gr.Interface(
        fn=chat,
        inputs="text",
        outputs="text",
        title="Chatbot",
        description="Ask what you want",
        live=True
    )
    iface.launch(share=True)

if __name__ == '__main__':
    main()