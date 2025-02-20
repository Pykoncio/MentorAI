import asyncio
import streamlit as st
import os
import sys

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(module_path)

from autogen_agentchat.messages import HandoffMessage
from main import research_swarm  # Usa el swarm que ya tienes definido
from autogen_agentchat.ui import Console

async def obtener_respuesta(mensaje_usuario: str) -> str:
    # Llama a la función asíncrona del swarm asignando el mensaje del usuario como tarea
    handoff_message = HandoffMessage(source="user", target="planner", content=mensaje_usuario)
    task_result = await Console(research_swarm.run_stream(task=handoff_message))
    good_messages = []
    for message in task_result.messages:
        if "[Function" not in message.content and "Transferred to user" not in message.content:
            good_messages.append(message)
    # Obtiene el último mensaje de la respuesta
    ultima_mensaje = good_messages[-1]
    if isinstance(ultima_mensaje, HandoffMessage):
        return ultima_mensaje.content
    return "Unknown answer."

async def main():
    st.title("MentorAI")
    mensaje_usuario = st.text_input("Hello! I'm your personal tutor. What topic or question do you need help with today?")
    if st.button("Send"):
        respuesta = await obtener_respuesta(mensaje_usuario)
        st.write("**Chatbot:**", respuesta)

if __name__ == "__main__":
    asyncio.run(main())