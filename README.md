# Standard Transformation Module

This is a **FastAPI**-based application that extracts **security requirements** from standard documents using **LLM (Large Language Model) processing**. The extracted requirements are then stored in **MongoDB**.

## 🚀 Features
- Extracts **security requirements** from provided text excerpts.
- Uses an **LLM model via Open WebUI API** for text processing.
- Stores extracted requirements in a **MongoDB database**.
- Provides a **FastAPI RESTful endpoint** for external integration.

---

## 📌 Requirements

- Python **3.8+**
- **MongoDB** (running locally or remotely)
- `.env` file with necessary API keys and MongoDB connection details.

---

## 🛠️ Installation

1️⃣ **Clone the repository**:
```sh
git clone https://github.com/certh-ai-and-softeng-group/standard-transformation-module.git
cd standard-transformation-module
```

2️⃣ **Create a virtual environment**:
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3️⃣ **Install dependencies**:
```sh
pip install -r requirements.txt
```

---

## 🛠️ Configuration

1️⃣ **Create a `.env` file** in the root directory:
```
MONGO_URL=mongodb://root:example@mongo:27017/?authSource=admin
OPENWEBUI_AUTH=your_openwebui_api_key
BASE_URL=http://your-webui-server:3000/api/chat/completions
```
Replace `your_openwebui_api_key` and `your-webui-server` with actual values.

2️⃣ **Ensure MongoDB is running**:
```sh
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=example mongo
```

---

## 🚀 Running the API

Run the FastAPI server:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at:
```
http://127.0.0.1:8000
```

---

## 📁 API Endpoints

### **1️⃣ Extract Requirements**
Extracts security requirements from a given text and stores them in MongoDB.

- **Endpoint**: `POST /extract-requirements/`
- **Request Body**:
  ```json
  {
    "standard": "ISO 27001",
    "excerpt": "All employees must follow the access control policy."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Requirements extracted successfully.",
    "inserted_id": "65a8c4e5b7d4b53e3c9fbc5a",
    "extracted_requirements": [
      "All employees must follow the access control policy."
    ]
  }
  ```

---

## 📂 Project Structure
```
💚 standard-transformation-module
👉📂 models
│   👉 ComplianceModel.py      # Pydantic model for MongoDB compliance storage
│   👉 database.py             # MongoDB connection handling
👉📂 services
│   👉 compliance_service.py   # Core logic for extracting requirements
👉📂 utils
│   👉 utils.py                # Helper functions (e.g., loading prompt wrapper)
👉📂 files
│   👉 prompt_wrapper.txt      # Template prompt for LLM
👉 .env                        # Environment variables (not committed)
👉 main.py                     # FastAPI application entry point
👉 requirements.txt             # Python dependencies
👉 README.md                    # This file
```

---

## 🐙 Running with Docker (Optional)

1️⃣ **Build the Docker image**:
```sh
docker build -t standard-transformation-module .
```

2️⃣ **Run the container**:
```sh
docker run -p 8000:8000 --env-file .env standard-transformation-module
```

---

## 🛠 Troubleshooting

- **MongoDB connection issues?**
  - Ensure MongoDB is running: `docker ps` or `systemctl status mongod`
  - Check if `MONGO_URL` in `.env` is correct.

- **OpenWebUI API issues?**
  - Ensure `BASE_URL` and `OPENWEBUI_AUTH` are correct in `.env`.

## Built with
<div align="center">
  <table>
    <tr>
      <td align="center">
        <img style="height:70px;" src="https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzdmy86qvblqmz3xfxlrr.png" alt="FastAPI"/>
      </td>
      <td align="center">
        <img style="height:70px;" src="https://www.python.org/static/img/python-logo.png" alt="Python"/>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img style="height:70px;" src="https://webimages.mongodb.com/_com_assets/cms/kuyjf3vea2hg34taa-horizontal_default_slate_blue.svg?auto=format%252Ccompress" alt="MongoDB"/>
      </td>
      <td align="center">
        <img style="height:70px;" src="https://upload.wikimedia.org/wikipedia/commons/e/ec/DeepSeek_logo.svg" alt="DeepSeek"/>
      </td>
    </tr>
    <tr>
      <td align="center" colspan="2">
        <img style="height:70px;" src="https://open-webui.com/wp-content/uploads/2024/09/Open-WebUI-Functions.png" alt="Open WebUI"/>
      </td>
    </tr>
  </table>
</div>


<hr/>
<div align="center">
  <img style="height:7em; width:auto;" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKW0vKZ0FDFUSADb3nqmQY08auPHSdVwQsOWtM8WOz&s"/>
  <img style="height:7em; width:auto;" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQODiKz9QcA8MsE0a0nmUn7xJELwDj48KWruyg8L_Bc&s"/>
</div>
<hr/>
