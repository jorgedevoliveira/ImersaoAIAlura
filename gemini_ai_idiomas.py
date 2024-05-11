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
def chatbot(prompt, history):
    chat = model.start_chat(history=[{"user": "", "bot": ""}] + history)  # Inicializa o histórico
    response = chat.send_message(prompt)
    history.append({"user": prompt, "bot": response.text})  # Adiciona a mensagem ao histórico
    return response.text

def main():
    st.title("Chatbot com GEMINI AI")
    st.markdown("Este é um chatbot alimentado por GEMINI AI, onde você pode praticar idiomas.")

    if "history" not in st.session_state:
        st.session_state["history"] = []  # Inicializa o histórico na sessão se não existir

    prompt = st.text_input("Você:", "")
    if st.button("Enviar"):
        if prompt.strip() != "":
            resposta_chatbot = chatbot(prompt, st.session_state["history"])
            st.text_area("Chatbot:", value=resposta_chatbot, height=100)
            # Limpa o campo de entrada após enviar a mensagem
            st.session_state["last_prompt"] = prompt
            st.text_input("Você:", value="", key="last_prompt")

    # Exibe o histórico do chat na tela
    st.subheader("Histórico do Chat")
    for message in st.session_state["history"]:
        st.text(f"Você: {message['user']}")
        st.text(f"Chatbot: {message['bot']}")
        st.text("-----")

if __name__ == "__main__":
    main()
