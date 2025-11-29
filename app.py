# STEP 1: Imports & Configuration
import streamlit as st
import ollama

# Configure the page title and header
st.set_page_config(page_title="P035: Streamlit Email Assistant", page_icon="📧")
st.title("📧 Local Email Responder (Llama 3)")

# STEP 2: Data/Input Preparation
# Capture the original email text from the user
original_email = st.text_area("Paste the original email here:", height=150)
# Capture the specific goal/tone for the response
response_goal = st.text_input(
    "Response Goal (e.g., 'Polite refusal', 'Accept meeting'):"
)


# STEP 3: Define the function to handle the LLM generation (Header Only)
# Define the function signature; logic will be implemented in Step 4
def generate_email(email_text, goal):
    """Generates an email response using the local Ollama model with a robust system prompt."""

    # We define a strict persona and set of rules for the AI
    system_prompt = (
        "You are a Senior Executive Assistant with expert business communication skills. "
        "Your task is to draft a professional email reply based EXACTLY on the user's Goal. "
        "\n\n"
        "RULES:\n"
        "1. TONE: Match the tone requested in the 'Goal' (e.g., strict, polite, empathetic).\n"
        "2. FORMAT: Output *only* the email draft. Do not include chatty conversational filler like 'Here is your draft'.\n"
        "3. STRUCTURE: Include a relevant Subject Line, Salutation, Body, and Sign-off.\n"
        "4. CLARITY: Be concise, direct, and avoid unnecessary jargon.\n"
    )

    # We structure the user input to clearly separate the 'Goal' from the 'Source Text'
    user_prompt = (
        f"### INSTRUCTIONS/GOAL:\n{goal}\n\n"
        f"### ORIGINAL RECEIVED EMAIL:\n{email_text}\n\n"
        f"### YOUR DRAFT RESPONSE:"
    )

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]


# STEP 5: Main Execution Block
# Create a button to trigger the generation; ensure inputs exist before calling the LLM
if st.button("Generate Reply"):
    if original_email and response_goal:
        st.write(generate_email(original_email, response_goal))
    else:
        st.warning("Please provide both the email content and your goal.")
