import requests, json


def dict_para_str(dicionario):
    itens_str = []
    
    for _, valor in dicionario.items():
        itens_str.append(valor)
    
    resultado_str = "\n".join(itens_str)
    return resultado_str

def tokenizer(text):
    """
    This function sends a POST request to a remote server to tokenize the given text and returns the number of tokens 
    as per the server's response.

    The function sends the text to be tokenized as JSON data in the body of the POST request. It includes the 'Content-Type' 
    header to specify that the request content type is JSON.

    The server is expected to process the request by tokenizing the text, and the function returns the server's response in 
    JSON format, which contains the number of tokens in the text under the 'return' key.

    Parameters:
    text (str): The text to be tokenized.

    Returns:
    dict: The server's response in JSON format. The response is expected to contain the number of tokens in the text 
        under the 'return' key.

    Example:
    >>> text = "Hello, world!"
    >>> print(tokenizer(text))
    {'return': '3'}
    # This assumes that the server successfully processed the request and found 3 tokens in the text.

    Note:
    This function requires an internet connection to send the POST request to the remote server.
    """
    data = {
        "text": text
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post('http://payconautomacoes.pythonanywhere.com/tokenizer', data=json.dumps(data), headers=headers)

    try:
        return response.json()['return']
    except Exception:
        return False
    
def cost_estimate_openai(tokens_or_text:str|int, model:str, prompts:dict|None):
    """Calcula o custo estimado com base no número de tokens e no modelo da OpenAI utilizado.

    Esta função estima o custo de uso dos modelos da OpenAI, considerando o número de tokens e o modelo específico utilizado. 
    O custo é calculado com base nas tarifas por mil tokens para cada modelo. Se prompts forem fornecidos, o comprimento total 
    dos prompts é adicionado ao número total de tokens.

    Args:
        tokens (int): O número de tokens utilizados na consulta.
        model (str): O nome do modelo da OpenAI utilizado.
        prompts (dict, optional): Um dicionário de prompts que serão enviados, usado para calcular o comprimento total em tokens.

    Returns:
        tuple: Uma tupla contendo o custo total estimado (como uma string formatada) e o número total de tokens.

    Modelos Disponíveis:
        - assistants
        - gpt-3.5-turbo-1106
        - gpt-3.5-turbo-instruct
        - gpt-4
        - gpt-4-32k
        - gpt-4-1106-preview

    Raises:
        Exception: Erros podem ocorrer se o modelo especificado não for suportado ou outros parâmetros forem inválidos.
    """

    if isinstance(tokens_or_text, str):
        tokens = int(tokenizer(tokens_or_text))
    elif isinstance(tokens_or_text, int):
        tokens = tokens_or_text

    if prompts is not None:
        prompts_len = len(dict_para_str(prompts))
        tokens = tokens + prompts_len
    if model == 'assistants':
        custo_por_mil = 0.01+0.03+0.20  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens
    if model == 'gpt-3.5-turbo-1106':
        custo_por_mil = 0.003  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens
    if model == 'gpt-3.5-turbo-instruct':
        custo_por_mil = 0.0015+0.0020  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens
    if model == 'gpt-4':
        custo_por_mil = 0.03+0.06  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens
    if model == 'gpt-4-32k':
        custo_por_mil = 0.06+0.12  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens
    if model == 'gpt-4-1106-preview':
        custo_por_mil = 0.01 + 0.03  # Custo por 1000 tokens
        custo_total = (tokens / 1000) * custo_por_mil
        return f'{custo_total:.3f}', tokens