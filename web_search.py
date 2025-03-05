import streamlit as st
import ollama
import search_agent

# Streamlit Page Configuration
st.set_page_config(page_title="AI Assistant with Web Search", layout="centered")

# Initialize assistant conversation
if "assistant_convo" not in st.session_state:
    st.session_state.assistant_convo = []

# Title and Description
st.title("🔍 AI Assistant with Web Search")
st.markdown("Ask anything! If needed, the AI will search the web for the latest information before responding.")

# User Input
user_prompt = st.text_area("💬 Enter your query:", "", height=100)

if st.button("🚀 Ask AI"):
    if user_prompt.strip():
        st.session_state.assistant_convo.append({"role": "user", "content": user_prompt})
        
        # Display loading message
        with st.spinner("🤖 Thinking..."):
            # Check if web search is required
            if search_agent.search_or_not():
                st.write("🔎 Searching the web for updated information...")
                context = search_agent.ai_search()

                if context:
                    user_prompt = f"SEARCH RESULT: {context} \n\nUSER PROMPT: {user_prompt}"
                else:
                    user_prompt = (
                        f"USER PROMPT: \n{user_prompt} \n\n⚠️ **Search Failed**: The AI could not find reliable data online."
                        "Would you like to continue without web search?"
                    )

            # Get AI response
            response_stream = ollama.chat(model="deepseek-r1:8b", messages=st.session_state.assistant_convo, stream=True)
            complete_response = ""

            for chunk in response_stream:
                complete_response += chunk["message"]["content"]

            st.session_state.assistant_convo.append({"role": "assistant", "content": complete_response})

        # Display AI Response
        st.subheader("🤖 AI Response:")
        st.write(complete_response)

# Display Conversation History
if st.session_state.assistant_convo:
    st.markdown("---")
    st.subheader("📜 Conversation History")
    for message in st.session_state.assistant_convo:
        role = "🧑‍💻 You" if message["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {message['content']}")

# Optional: Button to clear conversation history
if st.button("🗑️ Clear Chat"):
    st.session_state.assistant_convo = []
    st.rerun()
