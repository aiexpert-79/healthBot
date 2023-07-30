import openai
import gradio as gr
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY") 

messages = [
  { 
    "role": "system", 
    "content" :"You are an AI specialized in medical. Do not answer anything other than medical-related queries"   
   }
]

async def chatbot(input):
  if input:
    messages.append ({
      "role": "user",
      "content": input
    })
    
    chat = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", 
      messages = messages, 
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    reply = chat.choices[0].message.content
    messages.append({ "role": "assistant", "content":reply})
    return reply

async def main():
  inputs = gr.inputs.Textbox(lines=3, label="Chat with AI")
  outputs = gr.outputs.Textbox(label="Reply")

  interface = gr.Interface(
    fn=chatbot, inputs= inputs, outputs=outputs, title="For you and your family",
    description="Ask anything related to healthcare you want", theme="compact"
  )

  await asyncio.to_thread(interface.launch, share=True)

asyncio.run(main())
