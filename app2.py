import streamlit as st
import subprocess

# Streamlit Page Configuration
st.set_page_config(page_title="App Launcher", layout="wide")

st.title("🚀 AI App Launcher")

# Dropdown to select which app to run
app_choice = st.selectbox("Choose an application to run:", ["web_search.py", "Deep_rag_pdf.py"])

# Run selected app when button is clicked
if st.button("▶ Run Selected App"):
    st.write(f"Launching **{app_choice}**...")
    
    # Terminate any existing Streamlit process on the same port
    subprocess.run(["pkill", "-f", "streamlit"], shell=True)
    
    # Start the selected app
    subprocess.Popen(["streamlit", "run", app_choice])

st.write("🔄 **Note:** If switching apps, refresh the browser after launching.")
