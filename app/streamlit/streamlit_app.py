import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="MentorAI Chat", page_icon=":robot_face:")

# Título de la aplicación
st.title("MentorAI Chat")

# Campo de entrada para la pregunta
question = st.text_input("Escribe tu pregunta en inglés:")

# Incializar el sidebar
st.sidebar.title("Historial de chats")

# Para almacenar los diferentes chats con sus diferentes preguntas y respuestas,
# se debe crear una matriz cuadrada en donde en cada fila se almacene un diccionario
# con la pregunta y la respuesta.

# Variables de estado
if "list_chats" not in st.session_state and "answer" not in st.session_state and "chat_cont" not in st.session_state:
    st.session_state.list_chats = [[]]
    st.session_state.answer = None
    st.session_state.chat_cont = 0

# Botón para crear un nuevo chat
if st.sidebar.button("Nuevo chat") and st.session_state.chat_cont < len(st.session_state.list_chats):
    st.session_state.list_chats.append([])
    st.session_state.chat_cont += 1

# Botones para seleccionar el chat
for chat in st.session_state.list_chats:
    print(chat)
    st.sidebar.button(chat[0]['pregunta'], type="tertiary", key=f"chat_{st.session_state.chat_cont}")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if question:
        # Enviar la pregunta al endpoint /chat
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": question})
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.answer = f"Respuesta: {data['message']}"
            st.success(st.session_state.answer)

            # Guardamos en la lista de chats la pregunta y la respuesta
            st.session_state.list_chats[st.session_state.chat_cont].append({"pregunta": question, "respuesta": data["message"]})
            print(st.session_state.list_chats)
            print(st.session_state.chat_cont)
        else:
            st.session_state.answer = "Error al obtener la respuesta. Inténtalo de nuevo."
            st.error(st.session_state.answer)
    else:
        st.session_state.answer = "Por favor, escribe una pregunta."
        st.warning(st.session_state.answer)
    st.rerun()