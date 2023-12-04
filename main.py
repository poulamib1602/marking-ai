# # 
import streamlit as st
import requests

# Fetch CSRF token
csrf_token_url = "http://15.206.91.219/get-csrf-token/"
csrf_token = requests.get(csrf_token_url).json()['csrf_token']
print("csrf_token", csrf_token)
django_api_url = 'http://15.206.91.219/upload_pdf/'
# Streamlit app
# Set the sidebar title with larger and bolder styling
st.sidebar.markdown("<h1 style='font-size: 34px; font-weight: bold;'>MarkingAI</h1>", unsafe_allow_html=True)

# Place the title outside the sidebar
st.title("Upload File")

# Place the selectbox outside the sidebar
typ = st.selectbox("Who are you?", ("Teacher", "Student"))

# Place the file uploader outside the sidebar
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Create a submit button
if st.button("Submit"):
    if typ and pdf_file:
        # Extract PDF file name
        pdf_filename = pdf_file.name
        files = {'pdf_file': (pdf_filename, pdf_file, 'application/pdf')}
        headers = {'X-CSRFToken': csrf_token}

        # Create a placeholder for the spinner
        with st.spinner("Processing..."):
            # Send the file to the Django app
            response = requests.post(django_api_url, files=files, headers=headers, data={'type': typ})
            res_text = eval(response.text)
            print(res_text['response_msg'])

            # Display response message in a popup
            if response.status_code == 200:
                st.success(res_text['response_msg'])
            else:
                st.error(res_text['response_msg'])
