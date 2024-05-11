import streamlit as st
import google.generativeai as genai

# Configurando a API Key do GEMINI AI
GOOGLE_API_KEY = "AIzaSyCk282dAS15LSTOU7GOjsmWOkoFhmMoUlI"  # Substitua pela sua chave
genai.configure(api_key=GOOGLE_API_KEY)

# Configurações do modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

system_instruction = "Responda como um professor de idiomas, \n" \
                     "na primeira resposta, solicite o idioma que a pessoa quer praticar e que para encerrar o chat basta digitar 'sair',\n" \
                     "responda no idioma pt-br e no idioma solicitado no prompt\n\n"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

# Inicializa o chat fora da função para manter o histórico
chat = model.start_chat(history=[])

# Função para interagir com o chatbot
def chatbot(prompt):
    global chat  # Indica que estamos usando a variável chat global
    response = chat.send_message(prompt)
    return response.text

def main():
    st.title("Chatbot com GEMINI AI")
    st.markdown("Este é um chatbot alimentado por GEMINI AI, onde você pode praticar idiomas.")

    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe o histórico de mensagens
    for message in st.session_state.messages:
        st.text_area("Usuário:", value=message["user"], key=message["key"])
        st.text_area("Chatbot:", value=message["bot"], key=message["key"] + "_bot")

    # Input para o usuário
    prompt = st.text_input("Você:", "")
    if st.button("Enviar"):
        if prompt.strip() != "":
            # Adiciona a mensagem do usuário ao histórico
            st.session_state.messages.append({"user": prompt, "key": str(len(st.session_state.messages))})
            # Obtém a resposta do chatbot
            resposta_chatbot = chatbot(prompt)
            # Adiciona a resposta do chatbot ao histórico
            st.session_state.messages.append({"bot": resposta_chatbot, "key": str(len(st.session_state.messages))})
            # Limpa o input do usuário
            st.session_state.input_value = ""
            # Recarrega a página para exibir o histórico atualizado
            st.experimental_rerun()

        if prompt.strip() == "sair":
            st.session_state.messages = [] # reinicia o historico
            st.experimental_rerun() # reinicia a conversa

if __name__ == "__main__":
    main()
