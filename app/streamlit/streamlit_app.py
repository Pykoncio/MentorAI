import streamlit as st
import requests

st.set_page_config(page_title="MentorAI Chat", page_icon=":robot_face:")

st.title("MentorAI Chat")

st.sidebar.title("Chat History")

if "list_chats" not in st.session_state:
    st.session_state.list_chats = [[]] # Directamente meto aquí los mensajes de cada chat
if "actual_chat" not in st.session_state:
    st.session_state.actual_chat = 0

# Si el chat actual está guardado con mensajes, se puede iniciar uno nuevo
if st.sidebar.button("New chat", icon=":material/add:") and len(st.session_state.list_chats[st.session_state.actual_chat]) > 0:
    st.session_state.list_chats.insert(0, [])
    st.session_state.actual_chat = 0

# if "messages" not in st.session_state:
#     st.session_state.messages = []  
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

for message in st.session_state.list_chats[st.session_state.actual_chat]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("bot"):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me something"):
    st.session_state.current_question = prompt
    st.session_state.list_chats[st.session_state.actual_chat].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post("http://127.0.0.1:8000/chat", json={"message": st.session_state.current_question})            

    if response.status_code == 200:
        data = response.json()
        teacher = data.get("teacher", "Teacher")
        subject = data.get("subject", "Subject")
        message = data.get("message", "No answer")
        bot_response = f"**{teacher}:** {message}"
        
        st.session_state.list_chats[st.session_state.actual_chat].append({"role": "bot", "content": bot_response})

        with st.chat_message("Assistant", avatar="🤖"):
            st.markdown(bot_response)
        st.session_state.current_question = ""

    else:
        st.error("Error fetching the response. Please try again.")

for i in range(len(st.session_state.list_chats)):
    if len(st.session_state.list_chats[i]) > 0:
        if st.sidebar.button(st.session_state.list_chats[i][0]['content'], type="tertiary", key=f"chat_{i}"):
            print(f"Total de chats: {len(st.session_state.list_chats)}")
            print(f"Chat actual: {st.session_state.list_chats[st.session_state.actual_chat]}")

            # Si actualmente estoy en un chat nuevo sin mensajes, lo borro y paso al seleccionado en el sidebar
            if st.session_state.list_chats[st.session_state.actual_chat] == []:
                print("Borrando chat...")
                st.session_state.list_chats.pop(st.session_state.actual_chat)
                st.session_state.actual_chat = i - 1
            else:
                st.session_state.actual_chat = i
            st.rerun()