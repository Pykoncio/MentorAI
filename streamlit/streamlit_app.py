import asyncio
import streamlit as st
import os
import sys
import threading

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(module_path)

from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.ui import Console
from main import research_swarm  # Usa el swarm que ya tienes definido

def filtrar_mensajes_buenos(task_result):
    return [msg for msg in task_result.messages if not isinstance(msg.content, list) and "Transferred to user" not in msg.content]

# Obtener el event loop de Streamlit
if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
    threading.Thread(target=st.session_state.loop.run_forever, daemon=True).start()

# Configurar la sesión en Streamlit para almacenar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_message" not in st.session_state:
    st.session_state.last_message = None

st.title("MentorAI")

# Entrada de usuario para iniciar la investigación
user_input = st.text_input("Ingrese su solicitud:", key="user_input")
if st.button("Iniciar Investigación") and user_input:
    async def run_task():
        task_result = await Console(research_swarm.run_stream(task=user_input))
        st.session_state.messages.append(("system", f"Investigación iniciada: {user_input}"))
        st.session_state.last_message = task_result.messages[-1]
       
    asyncio.run(run_task()) 

# Mostrar mensajes previos
for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")

# Manejar respuestas del usuario si es necesario
if isinstance(st.session_state.last_message, HandoffMessage) and st.session_state.last_message.target == "user":
    user_reply = st.text_input("Responda al agente:", key="user_reply")
    if st.button("Enviar Respuesta") and user_reply:
        async def respond():
            handoff_message = HandoffMessage(
                source="user",
                target=st.session_state.last_message.source,
                content=user_reply
            )
            task_result = await Console(research_swarm.run_stream(task=handoff_message))
            st.session_state.messages.append(("user", user_reply))
            st.session_state.last_message = task_result.messages[-1]

        asyncio.run(respond()) 
    st.rerun()