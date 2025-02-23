import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="MentorAI Chat", page_icon=":robot_face:")

# Título de la aplicación
st.title("MentorAI Chat")

# Campo de entrada para la pregunta
question = st.text_input("Escribe tu pregunta en inglés:")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if question:
        # Enviar la pregunta al endpoint /chat
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": question})
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"Respuesta: {data['message']}")
        else:
            st.error("Error al obtener la respuesta. Inténtalo de nuevo.")
    else:
        st.warning("Por favor, escribe una pregunta.")