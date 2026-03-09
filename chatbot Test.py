from ollama import chat
model='phi3:mini'
while True:
    prompt = input('Hisham:')
    if prompt.lower() in ['bye', 'exit']:
        break
    messages=[
        {'role': 'user', 'content': prompt}
    ]


    response = chat(model = model, messages = messages)
    assistant_response = response.message.content
    messages = [
            {'role': 'assistant', 'content': assistant_response}
    ]
    print(f'Asistant: {assistant_response}')
