from pyexpat.errors import messages

from ollama import chat

history = []
model = 'phi3:mini'
prompt = input('Hisham: ')

def get_user_input():
    return prompt


def add_user_input(message, history):
    history.append(messages=({
        'role': 'user',
        'content': prompt
    }))


def get_model_response(model, history):
    response = chat(model=model, message=messages)
    return response.message.content


def get_assistant_response(history, assistant_response):
    history.append(message=({
        'role': 'assistant',
        'content': assistant_response
    }))
    return assistant_response


def print_reply(assistant_response):
    print(f'Assistant: {assistant_response}')

    while True:
        if input.lower() in ['exit', 'bye']:
            break


get_user_input()
add_user_input(prompt, history)
assistant_response = get_model_response(model, history)
get_assistant_response(history, assistant_response)
print_reply(assistant_response)
