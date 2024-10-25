import requests
from funcspy.python_funcs.python_funcs import *
from openai import OpenAI

def api_chat_completions(api_key:str, model='gpt-4-turbo', messages:list[dict]=[]):
    """
    This function sends a chat completion request to the OpenAI API.
    
    Usage:
    ```
        api_key = 'your_api_key'
        model='gpt-4-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant. (OR YOUR QA)"},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        response = api_chat_completions(api_key, model, messages)
    ```
    """
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content


def api_image_generation(api_key:str, prompt:str, model='dall-e-3', size='1024x1024', quality='standard', n=1):
    """
    This function sends an image generation request to the OpenAI API.
    
    Usage:
    ```
        api_key = 'your_api_key'
        model='dall-e-3',
        prompt='a photograph of an astronaut riding a horse'
        size='1024x1024'
        quality='hd'
        response = api_image_generation(api_key, model, prompt, size, quality)
    ```
    """
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )

    return response.data[0].url

def api_vision(api_key:str, messages:str, model='gpt-4-turbo'):
    """
    This function use GPT-4 Turbo with Vision allows the model to take in images and answer questions about them.
    
    Usage:
    ```
        api_key = 'your_api_key'
        messages={
            "role": "user",
            "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
                "type": "image_url",
                "image_url": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
            },
        ],
    }
        response = api_vision(api_key, messages, model)
    ```
    """
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
    )
    
    return response.choices[0]


def api_audio_transcription(api_key:str, file_path:str, model='whisper-1'):
    """
    This function sends an audio transcription request to the OpenAI API.
    
    Usage:
    ```
        api_key = 'your_api_key'
        file_path = 'audio_file.mp3'
        response = api_audio_transcription(api_key, file_path)
    ```
    """
    client = OpenAI(api_key=api_key)
    response = client.audio.transcriptions.create(file=file_path, model=model)
    return response.text
