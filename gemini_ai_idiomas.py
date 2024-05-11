from IPython.display import display
from IPython.display import Markdown
import textwrap


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


import google.generativeai as genai

# Importar a API Key armazenada nos secrets do Colab
from google.colab import userdata



# Configurando a API Key do GEMINI AI

GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
]

system_instruction = "Responda como um professor de idiomas, \nna primeira resposta, solicite o idioma que a pessoa quer praticar e que para encerrar do chat basta digitar sair,\nresponda no idioma pt-br e no idioma solicitado no promp\n\n"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])
chat

prompt = input("Prompt: ")

while prompt != "sair":
  response = chat.send_message(prompt)
  display(to_markdown(response.text))
  prompt = input("Prompt: ")
