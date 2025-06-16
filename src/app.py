import streamlit as st
from rag_logic import answer_with_rag  # Import our backend logic

# --- Page Configuration ---
# This is the first Streamlit command to run, and it should only be run once.
st.set_page_config(
    page_title="Angel One Support Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- UI Elements ---
st.title("🤖 Angel One Support Chatbot")
st.caption("This chatbot is powered by Google Gemini and can only answer questions based on its knowledge base.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your account, brokerage, or more..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = answer_with_rag(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})