FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install needed Python packages
RUN pip install --no-cache-dir fastapi uvicorn pydantic python-dotenv

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install all dependencies explicitly
RUN pip install --no-cache-dir \
    annotated-types==0.7.0 \
    anyio==4.5.2 \
    certifi==2025.1.31 \
    charset-normalizer==3.4.1 \
    click==8.1.8 \
    dnspython==2.7.0 \
    fastapi==0.110.0 \
    h11==0.14.0 \
    idna==3.7 \
    motor==3.3.2 \
    pydantic==2.5.3 \
    pydantic-core==2.14.6 \
    pymongo==4.11.1 \
    python-dotenv==1.0.1 \
    requests==2.32.3 \
    setuptools==75.8.0 \
    sniffio==1.3.1 \
    starlette==0.36.3 \
    typing_extensions==4.13.0 \
    urllib3==2.3.0 \
    uvicorn==0.24.0.post1 \
    wheel==0.45.1


# Copy your app files into the container
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
