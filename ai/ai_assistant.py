import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def query_llm_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        result = response.json()
        st.write("🧪 Debug Ollama Result:", result)  # <--- Add this
        return result["response"]
    except Exception as e:
        return f"[Assistant Error] {e}"


def ai_festival_assistant():
    st.subheader("🤖 AI Festival Assistant")
    st.markdown("Ask me anything about Indian festivals!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for entry in st.session_state.chat_history:
        st.chat_message(entry["role"]).markdown(entry["content"])

    user_input = st.chat_input("Ask about a festival, region, or date...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            # You could combine history here if needed
            reply = query_llm_ollama(user_input)
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
