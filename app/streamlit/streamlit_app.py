import streamlit as st
import requests
import pandas as pd
import sys
import re
import os
import csv
import pymysql
from sqlalchemy import text
import os
import sys
import pathlib
core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(core_path)
from config import settings

def remove_markdown(text):
   # Remove inline code formatting and return only the inner text.
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # Remove bold/italic formatting by removing ** or __ markers around text.
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    
    # Remove Markdown headers (e.g., "# Header") by matching 1 to 6 '#' symbols
    text = re.sub(r'^\s{0,3}#{1,6}\s*', '', text, flags=re.MULTILINE)
    
    # Remove blockquote markers ('>') at the beginning of a line.
    text = re.sub(r'^\s{0,3}>\s?', '', text, flags=re.MULTILINE)
    
    # Remove list markers for unordered lists (e.g., '-', '*', '+') at the beginning of a line.
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    
    # Remove numerical list markers (e.g., "1.", "2)") at the beginning of a line.
    text = re.sub(r'^\s*\d+[\.\)]\s+', '', text, flags=re.MULTILINE)
    
    # Remove horizontal rule lines made entirely of dashes.
    text = re.sub(r'\n-{3,}\n', '\n', text)
    
    # Remove horizontal rule lines made entirely of asterisks.
    text = re.sub(r'\n\*{3,}\n', '\n', text)
    
    # Remove backslashes used to escape special Markdown characters.
    text = re.sub(r'\\([\\`*_{}\[\]()#+\-.!])', r'\1', text)
    
    return text

def cargar_css(path):
    with open(path) as f:
        st.html(f"<style>{f.read()}</style>")

pymysql.install_as_MySQLdb()

st.set_page_config(page_title="MentorAI Chat", page_icon=":robot_face:")

path = pathlib.Path("app/streamlit/styles/styles.css")
cargar_css(path)

st.title("MentorAI Chat")

st.sidebar.title("Chat History")

if "list_chats" not in st.session_state:
    st.session_state.list_chats = [[]] 
if "actual_chat" not in st.session_state:
    st.session_state.actual_chat = 0

if st.sidebar.button("New chat", icon=":material/add:") and len(st.session_state.list_chats[st.session_state.actual_chat]) > 0:
    st.session_state.list_chats.insert(0, [])
    st.session_state.actual_chat = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

conn = st.connection("sql",
    dialect="mysql",
    host=settings.MYSQL_HOST,
    username=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DATABASE)

for message in st.session_state.list_chats[st.session_state.actual_chat]:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("bot", avatar="🤖"):
            st.markdown(message["content"], )

if prompt := st.chat_input("Ask me something", key="chat_input"):
    st.session_state.current_question = prompt
    st.session_state.list_chats[st.session_state.actual_chat].append({"role": "user", "content": prompt})

    create_table = text("""CREATE TABLE IF NOT EXISTS messages (
               id INT AUTO_INCREMENT PRIMARY KEY,
               role VARCHAR(50) NOT NULL,
               content VARCHAR(1000) NOT NULL);""")
    
    clean_prompt = remove_markdown(prompt)

    insert = text(f"""INSERT INTO messages (role, content) VALUES ("user", "{clean_prompt}")""")

    with conn.session as session:
        session.execute(create_table)
        session.commit()
        session.execute(insert)
        session.commit()

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = requests.post("http://fastapi:8000/chat", json={"message": st.session_state.current_question})            

    if response.status_code == 200:
        data = response.json()
        teacher = data.get("teacher", "Teacher")
        subject = data.get("subject", "Subject")
        message = data.get("message", "No answer")
        bot_response = f"**{teacher}:** {message}"
        
        st.session_state.list_chats[st.session_state.actual_chat].append({"role": "bot", "content": bot_response})

        insert = text("INSERT INTO messages (role, content) VALUES (:role, :content)")
        clean_message = remove_markdown(message[:1000])

        with conn.session as session:
            session.execute(insert, {"role": "bot", "content": clean_message})
            session.commit()

            engine = session.get_bind()
            df = pd.read_sql("SELECT role, content FROM messages", engine)
            df['content'] = df['content'].apply(remove_markdown)
            output_file = "output/messages_output.csv"
            df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

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

            if st.session_state.list_chats[st.session_state.actual_chat] == []:
                print("Borrando chat...")
                st.session_state.list_chats.pop(st.session_state.actual_chat)
                st.session_state.actual_chat = i - 1
            else:
                st.session_state.actual_chat = i
            st.rerun()
