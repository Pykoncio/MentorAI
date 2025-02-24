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

"""Para almacenar los diferentes chats con sus diferentes preguntas y respuestas,
se debe crear una matriz cuadrada en donde en cada fila se almacene un diccionario
con la pregunta y la respuesta."""

# Lista de chats creados
if "list_chats" not in st.session_state:
    st.session_state.list_chats = []
    st.session_state.answer = None

for chat in st.session_state.list_chats:
    st.sidebar.button(chat, type="tertiary")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if question:
        # Enviar la pregunta al endpoint /chat
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": question})
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.answer = f"Respuesta: {data['message']}"
            st.success(st.session_state.answer)

            # Almacenamos la pregunta en el historial
            st.session_state.list_chats.append(question)
        else:
            st.session_state.answer = "Error al obtener la respuesta. Inténtalo de nuevo."
            st.error(st.session_state.answer)
    else:
        st.session_state.answer = "Por favor, escribe una pregunta."
        st.warning(st.session_state.answer)
    st.rerun()