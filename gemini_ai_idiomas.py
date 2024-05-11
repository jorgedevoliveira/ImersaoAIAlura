import streamlit as st
import google.generativeai as genai

# Configurando a API Key do GEMINI AI
GOOGLE_API_KEY = "AIzaSyCk282dAS15LSTOU7GOjsmWOkoFhmMoUlI"
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

# Função para interação com o chatbot
def chatbot(prompt, chat_state=None):
    if chat_state is None:
        chat_state = {"history": []}

    chat = model.continue_chat(chat_state["history"])  # Continua a conversa a partir do estado anterior
    response = chat.send_message(prompt)
    
    chat_state["history"].append({"role": "system", "content": prompt})
    chat_state["history"].append({"role": "user", "content": response.text})

    return response.text, chat_state

def main():
    st.title("Chatbot com GEMINI AI")
    st.markdown("Este é um chatbot alimentado por GEMINI AI, onde você pode praticar idiomas.")

    chat_state = st.session_state.get("chat_state", None)  # Recupera o estado da conversa da sessão
    
    if chat_state is None or "history" not in chat_state:
        chat_state = {"history": []}

    prompt = st.text_input("Você:", "")
    if st.button("Enviar"):
        if prompt.strip() != "":
            resposta_chatbot, chat_state = chatbot(prompt, chat_state)
            st.text_area("Chatbot:", value=resposta_chatbot, height=100)
    
    # Atualiza o estado da conversa na sessão
    st.session_state["chat_state"] = chat_state

if __name__ == "__main__":
    main()# Função para interação com o chatbot
def chatbot(prompt, chat_state=None):
    if chat_state is None:
        chat_state = {"history": []}

    chat = model.continue_chat(chat_state["history"])  # Continua a conversa a partir do estado anterior
    response = chat.send_message(prompt)
    
    chat_state["history"].append({"role": "system", "content": prompt})
    chat_state["history"].append({"role": "user", "content": response.text})

    return response.text, chat_state

def main():
    st.title("Chatbot com GEMINI AI")
    st.markdown("Este é um chatbot alimentado por GEMINI AI, onde você pode praticar idiomas.")

    chat_state = st.session_state.get("chat_state", None)  # Recupera o estado da conversa da sessão
    
    if chat_state is None or "history" not in chat_state:
        chat_state = {"history": []}

    prompt = st.text_input("Você:", "")
    if st.button("Enviar"):
        if prompt.strip() != "":
            resposta_chatbot, chat_state = chatbot(prompt, chat_state)
            st.text_area("Chatbot:", value=resposta_chatbot, height=100)
    
    # Atualiza o estado da conversa na sessão
    st.session_state["chat_state"] = chat_state

if __name__ == "__main__":
    main()
