from groq import Groq

client = None
model = None



def set_groq( key: str):
    """
    Set up the Groq client with the API key from environment variables.
    """
    global client
    client = Groq(api_key=key)


def set_model(model_name: str):
    """
    Set the model to be used for autocompletion.
    :param model_name: The name of the model to use.
    """
    global model
    model = model_name

def get_autocompletion(system_message: str, user_message):
    """
    Get autocompletion from Groq AI.
    :param prompt: The prompt to send to the AI model.
    :return: The AI's response.
    """
    if client is None:
        raise ValueError("Groq client is not initialized. Please call set_groq() with a valid API key.")
    if model is None:
        raise ValueError("Model is not set. Please call set_model() with a valid model name.")

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        model=model,
    )
    return str(response.choices[0].message.content)

def get_groq_autocompletion( key, model ):
    """
    Get autocompletion from Groq AI.
    :param key: The API key for Groq.
    :param model: The model to use for autocompletion.
    :return: A function that takes a system message and user message and returns the AI's response.
    """
    set_groq(key)
    set_model(model)
    return get_autocompletion

