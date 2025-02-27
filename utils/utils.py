from fastapi import HTTPException


def load_prompt_wrapper():
    """
    Reads the prompt wrapper from 'prompt_wrapper.txt'
    """
    try:
        with open("./files/prompt_wrapper.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Prompt wrapper file not found.")