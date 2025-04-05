from openai import OpenAI
import streamlit as st

st.title("HEALTH SYMPTOM CHECKER")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the OpenAI model for the conversation
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize session state for messages if not already
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System prompt to restrict the model to medical domain only
system_prompt = {
    "role": "system",
    "content": """
    You are a helpful assistant in the medical domain. You can only discuss health-related topics, such as medical symptoms, conditions, treatments, and anything else related to human health. 
    You should not engage in any conversations that are outside of the medical field, such as discussing technology, politics, sports, or other unrelated subjects.
    """

}

# Take input from the user
if prompt := st.chat_input("Please describe your symptoms or concerns:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add the system message to ensure the model stays focused on health topics
    st.session_state.messages.append(system_prompt)

    # Generate the assistant's response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Process the streamed response from OpenAI
        response = st.write_stream(stream)

    # Append the assistant's response to the conversation
    st.session_state.messages.append({"role": "assistant", "content": response})
