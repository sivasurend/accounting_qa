import os
import streamlit as st
import openai
from lyzr import QABot

# Set your OpenAI API key
openai.api_key = st.secrets.openai_api_key
os.environ['OPENAI_API_KEY'] = st.secrets.openai_api_key


st.image('./Lyzr Logo 250px by 250px.png')

# Streamlit page configuration
st.title("Accounting QA Bot with Lyzr SDK")

# File uploader widget
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    return None

# Function to get example from GPT-4
def get_example(question, answer):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Accountant with good knowledge of accounting principles and examples. Provide an intelligent example based on the following question and answer."
            },
            {
                "role": "user",
                "content": f"Question: {question}\nAnswer: {answer}\n\nGive the example in less than 500 words"
            }
        ],
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    return response.choices[0].message['content']

# Save the uploaded file and initialize the QABot
if uploaded_file is not None:
    filename = save_uploaded_file(uploaded_file)
    
    # Initialize the QABot with the uploaded PDF file
    qa_bot = QABot.pdf_qa(input_files=[filename])

    # Text input for user question
    user_question = st.text_input("Enter your question")

    # Button to get the answer
    if st.button("Get Answer"):
    if user_question:
        # Ask the question to the QABot
        answer = qa_bot.query(user_question).response

        # Get example from GPT-4
        example = get_example(user_question, answer)

        # Combine answer and example into a single string
        combined_response = f"**Answer:**\n{answer}\n\n**Example:**\n{example}"

        # Display the combined response
        st.write(combined_response)
    else:
        st.write("Please enter a question to get an answer.")
