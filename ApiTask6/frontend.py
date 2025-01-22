import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("OCR Processor")

uploaded_file = st.file_uploader("Load your file", type=["jpg", "png", "jpeg", "tiff"])

lang = st.text_input("Type language (example, 'rus+eng/rus/eng')", value="rus+eng")

result_placeholder = st.empty()

if st.button("Process the image"):
    if uploaded_file is not None:
        with st.spinner("Processing the image..."):
            files = {"file": uploaded_file}
            try:
                response = requests.post(f"{API_URL}/process?lang={lang}", files=files)
                response_data = response.json()
                if response.status_code == 200:
                    task_id = response_data["task_id"]
                    st.success(f"Task created. ID: {task_id}")
                    st.session_state["last_task_id"] = task_id
                else:
                    st.error(f"Error: {response_data.get('detail', 'UNKNOWN')}")
            except Exception as e:
                st.error(f"Server error: {e}")


task_id = st.text_input("Input task ID to check status")
if st.button("Check Status") or "last_task_id" in st.session_state:
    if not task_id and "last_task_id" in st.session_state:
        task_id = st.session_state["last_task_id"]

    if task_id:
        with st.spinner("Checking status..."):
            try:
                response = requests.get(f"{API_URL}/status/{task_id}")
                response_data = response.json()
                if response.status_code == 200:
                    if response_data["status"] == "done":
                        result = response_data["result"]
                        st.success("Task completed!")
                        result_placeholder.text_area("OCR Result:", result, height=200)
                    elif response_data["status"] == "work":
                        st.info("Task is still in progress. Please check back later.")
                    else:
                        st.error(f"Task status: {response_data['status']}")
                else:
                    st.error(f"Error: {response_data.get('detail', 'UNKNOWN')}")
            except Exception as e:
                st.error(f"Server error: {e}")