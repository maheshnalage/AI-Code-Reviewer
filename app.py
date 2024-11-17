import streamlit as st
import openai
import google.generativeai as genai

# Initialize API keys
openai.api_key = "your api key"
genai.configure(api_key="your api key")

# Function to get code review from OpenAI (GPT)
def openai_code_review(user_code):
    response = openai.Completion.create(
        engine="code-davinci-002",  # You can use other models depending on the requirements
        prompt=f"Please review the following Python code and identify potential bugs and suggest improvements:\n\n{user_code}",
        max_tokens=150,
        temperature=0.3,
    )
    return response.choices[0].text.strip()

# Function to get code review from Google AI (Generative Language)
def googleai_code_review(user_code):
    sys_prompt = """You are an AI Code Reviewer. Your task is to analyze Python code for errors, inefficiencies, 
                    and potential bugs, and provide a revised version of the code with suggestions for improvement."""
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

    response = model.generate_content(user_code)

    # Extracting the review feedback and fixed code
    if response and response.candidates:
        feedback = response.candidates[0].content.parts[0].text
        return feedback
    else:
        return "No feedback available."

# Streamlit App Interface
st.title("AI Code Reviewer")

# Code Input Section
st.subheader("Enter your Python code for review:")
user_code = st.text_area("Paste your Python code here:", height=300)

# Syntax Highlighting for the entered code (Using Streamlit’s Markdown rendering)
if user_code:
    st.markdown(f"```python\n{user_code}\n```")

# Code Review Model Option
review_option = st.selectbox("Select AI Model for Code Review", ["OpenAI", "Google AI"])

# Initialize feedback variable
feedback = None

# Button to trigger review
if st.button("Review Code"):
    if user_code:
        with st.spinner("Reviewing your code..."):
            if review_option == "OpenAI":
                feedback = openai_code_review(user_code)
                st.subheader("OpenAI Review Feedback:")
                st.write(feedback)
            elif review_option == "Google AI":
                feedback = googleai_code_review(user_code)
                st.subheader("Google AI Review Feedback:")
                st.write(feedback)
    else:
        st.error("Please enter Python code to review.")

# Allow users to edit and re-submit code based on feedback if feedback is available
if feedback:
    if st.checkbox("Edit code based on feedback"):
        fixed_code = st.text_area("Fixed Code:", value=feedback, height=300)
        if st.button("Submit Fixed Code"):
            st.success("Your fixed code has been submitted!")
            # Here, you can add further functionality to handle the submission, e.g., saving to a file or database.
