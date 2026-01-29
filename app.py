import streamlit as st
from groq import Groq
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant")
st.title("🎓 AI Student Study Assistant ")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📄 PDF Summary", "📝 MCQ Generator"])

# -------- TAB 1: CHAT --------
with tab1:
    question = st.text_input("Ask any academic question:")

    if st.button("Ask AI"):
        if question:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a helpful student study assistant."},
                        {"role": "user", "content": question}
                    ]
                )
                st.success(response.choices[0].message.content)

# -------- TAB 2: PDF SUMMARY --------
with tab2:
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if st.button("Summarize PDF"):
            with st.spinner("Summarizing..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user", "content": "Summarize this in simple student notes:\n" + text}
                    ]
                )
                st.success(response.choices[0].message.content)

# -------- TAB 3: MCQ GENERATOR --------
with tab3:
    topic = st.text_input("Enter topic for MCQs:")

    if st.button("Generate MCQs"):
        with st.spinner("Generating MCQs..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": f"Generate 5 MCQs with answers on {topic}"}
                ]
            )
            st.success(response.choices[0].message.content)

st.markdown("---")
st.markdown("Built by **Jagan** | AI Study Assistant using Groq LLaMA 3.1")

