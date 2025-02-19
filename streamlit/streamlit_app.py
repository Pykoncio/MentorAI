import streamlit as st

def set_title(title: str):
    st.title(title)

def write_task():
    return st.text_input("Please select a task")

def show_message(message: str):
    st.write(message)