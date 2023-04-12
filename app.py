import openai
import random
import streamlit as st
from streamlit_chat import message
random1 = random.randrange(1,1000)
random2 = random.randrange(1,1000)

def get_api_key():
    api_key = st.sidebar.text_input("Enter your API key:")
    return api_key

# Setting page title and header
st.set_page_config(page_title="RTBRPG", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Random Text-Based RPG (Post-Apocalyptic) Type 'Start'</h1>", unsafe_allow_html=True)

# Set org ID and API key
openai.organization = ""
api_key = get_api_key()
if api_key:
    openai.api_key = api_key
else:
    openai.api_key = ""

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "Take the role of a text-base game, similar to old-school MUD games. The game should simulate the experience of a post-apocalyptic wasteland inspired by the Fallout series. You should give the player a few prompts for each choice they need to make in the game, but wait for them to respond before continuing. The player can choose one of your prompts, or write their own."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
#st.sidebar.title("")
model_name = "GPT-4"
counter_placeholder = 0
#counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = 0

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    #counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    #print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, avatar_style="adventurer", seed=random1, key=str(i) + '_user')
            message(st.session_state["generated"][i], avatar_style="adventurer", seed=random2, key=str(i))
            #st.write(
            #    f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            #counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
