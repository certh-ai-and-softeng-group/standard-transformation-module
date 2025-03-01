import os
from pathlib import Path
from fastapi import HTTPException

def load_prompt_wrapper():
    """
    Reads the prompt wrapper from 'files/prompt_wrapper.txt' with proper encoding
    based on OS (Windows/Linux) and dynamically locates the file.
    """
    try:
        # Dynamically find project root (assumes script is running inside project)
        project_root = Path(__file__).resolve().parent.parent  # Move up one level
        file_path = project_root / "files" / "prompt_wrapper.txt"  # Adjust path

        # Determine encoding based on OS
        encoding = "utf-8-sig" if os.name == "nt" else "utf-8"

        # Open file with proper encoding
        with file_path.open("r", encoding=encoding) as file:
            return file.read()

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Prompt wrapper file not found at {file_path}")

    except UnicodeDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Encoding error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading prompt wrapper file: {str(e)}")
