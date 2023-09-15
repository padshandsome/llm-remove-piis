import streamlit as st
import base64 

def render_file(bytes_data): 
    col1, col2, col3, col4 = st.columns([6,0.1,6,0.1])
    with col1:
        st.text("Original Document:")
        base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="600px" height="800px" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    with col2:
        st.empty()

    with col3:
        st.text("De-identified Document:")

        with open("data/filtered/temp_masked.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="600px" height="800px" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    with col4:
        st.empty()