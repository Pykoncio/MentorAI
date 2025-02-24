import streamlit as st
import requests

st.set_page_config(page_title="MentorAI Chat", page_icon=":robot_face:")

st.title("MentorAI Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []  
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("bot"):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me something"):
    st.session_state.current_question = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post("http://127.0.0.1:8000/chat", json={"message": st.session_state.current_question})            

    if response.status_code == 200:
        data = response.json()
        teacher = data.get("teacher", "Teacher")
        subject = data.get("subject", "Subject")
        message = data.get("message", "No answer")
        bot_response = f"**{teacher}:** {message}"
        
        st.session_state.messages.append({"role": "bot", "content": bot_response})

        with st.chat_message("Assistant", avatar="🤖"):
            st.markdown(bot_response)
        st.session_state.current_question = ""

    else:
        st.error("Error fetching the response. Please try again.")