LangChain Testing API
A modular Python project for experimenting with LangChain and large language model (LLM) workflows. The application exposes task-focused REST endpoints through FastAPI and uses reusable prompt files, Pydantic schemas, and a shared LLM configuration.
Features
- Task 1 — Text transformation: Summarize, translate, or change the tone of supplied text.
- Task 2 — Resume parsing: Extract structured resume information from text or an uploaded PDF.
- Task 3 — Question routing: Classify a question as coding, math, or general, then send it to the corresponding prompt chain.
- Task 4 — Social content generation: Generate a tweet, LinkedIn caption, and hashtags for a topic in parallel.
- Task 5 — Safe JSON generation: Ask the model for JSON and attempt to repair the response if it is invalid.
- Health endpoint: Check whether the API is running.

Requirements
- Python 3.10 or newer
- An OpenRouter API key and a model identifier available to your account
- Internet access to call hosted models
The project also declares Hugging Face settings in config.py. The shared chat model in LLMs/base.py currently uses the OpenRouter-compatible API.
Setup
1. Clone or download the repository
Open the project folder in VS Code, then open a terminal in the project root (the folder containing main.py).
2. Create and activate a virtual environment
Windows PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
If activation is blocked by your PowerShell execution policy, run the environment's Python directly:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install fastapi "uvicorn[standard]" pydantic-settings pypdf python-multipart
4. Configure environment variables
Create a .env file in the project root, next to config.py. Add your own credentials and model identifiers:

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_POOLSIDE_MODEL=your_openrouter_model_identifier
OPENROUTER_GEMMA_MODEL=your_openrouter_model_identifier
HUGGINGFACEHUB_ACCESS_TOKEN=your_hugging_face_token
HUGGINGFACE_FASTCONTEXT_MODEL=your_hugging_face_model_identifier
EMBEDDING_MODEL=your_embedding_model_identifier
TEMPERATURE=0.8

Replace the example values with valid values from your provider. The shared client currently uses OPENROUTER_API_KEY, OPENROUTER_GEMMA_MODEL, and TEMPERATURE.
Security: Never commit your .env file or publish API keys. If a real key has been exposed, revoke it with the provider and generate a replacement. Keep .env out of version control.

5. Run the API
From the project root, run:
uvicorn main:app --reload
The development server should start at http://127.0.0.1:8000.
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health
--reload is intended for local development.
API Endpoints
You can try the endpoints from Swagger UI at http://127.0.0.1:8000/docs. Request and response schemas are defined in the task folders.
Health Check
GET /health

Checks whether the API is running.

Example response:
{
  "status": "ok"
}
Task 1 — Text Transformation
POST /transform

Supports text actions such as summarize, translate, and tone-shift.

Example request:
{
  "action": "summarize",
  "text": "Paste the text you want to summarize here.",
  "instruction": "Summarize it in three concise bullet points."
}
The response contains a response string.
Task 2 — Resume Parsing
POST /parse-resume

Accepts resume text as JSON:
{
  "resume": "Paste the resume text here."
}
The response contains structured resume fields, such as the candidate's name, skills, years of experience, and most recent role.

POST /parse-resume-file

Accepts a PDF file as multipart form data. The application extracts selectable text from the PDF before passing it to the resume parser. OCR for scanned/image-only PDFs is not included.
Task 3 — Question Routing
POST /ask

Classifies a question as coding, math, or general, then uses the matching prompt to generate an answer.

Example request:
{
  "question": "Explain the difference between a list and a tuple in Python."
}
The response contains the predicted category and the generated answer.
Task 4 — Social Content Generation
POST /generate-post

Generates social media content for a supplied topic.

Example request:
{
  "topic": "Why learning Python is useful for beginners"
}
The response contains a tweet, a LinkedIn caption, and a list of hashtags. The three content chains are invoked in parallel.
Task 5 — Safe JSON Generation
POST /safe-json

Asks the model to return JSON and attempts to repair the response if parsing fails.

Example request:
{
  "prompt": "Create a JSON object for a fictional book with title, author, and publication_year."
}
The response wraps the parsed JSON object in a data field. This is a best-effort repair process; valid JSON and semantic correctness are not guaranteed.
Testing
1. Start the server with uvicorn main:app --reload.
2. Open http://127.0.0.1:8000/docs.
3. Expand the endpoint you want to test.
4. Click Try it out.
5. Enter the request body or select a PDF file, then click Execute.
6. Review the HTTP status code and response body.
Notes and Limitations
- Run the API from the project root so relative prompt paths resolve correctly.
- PDF upload currently expects a PDF file, not a DOCX file.
- Scanned PDFs may not produce text because OCR is not implemented.
- Model output can be inaccurate. Validate generated resume data and JSON before relying on them.
- Provider credentials and access to the configured model are required. API calls may incur usage charges.
- The project archive does not include a license file. Add a LICENSE file if you intend to publish or distribute the project.
Troubleshooting
Missing Python module

Activate the intended virtual environment and install the dependencies. In VS Code, check that the selected Python interpreter points to the project's .venv.

Configuration or validation error on startup

Check that .env exists in the project root and that required variables are present and correctly named.

Provider authentication or model error

Verify OPENROUTER_API_KEY and OPENROUTER_GEMMA_MODEL. Confirm that the selected model is available to your OpenRouter account.

PDF upload error

Confirm that python-multipart is installed and that the uploaded file is a valid PDF.

Prompt file not found

Run the server from the project root, or adjust the code to resolve prompt paths relative to the Python source files.
