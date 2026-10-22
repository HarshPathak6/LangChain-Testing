LangChain Testing API
A modular Python project for experimenting with LangChain and
large-language-model workflows. The application exposes five
task-focused REST API groups through FastAPI and uses reusable prompt
files, Pydantic schemas, and a shared LLM configuration.
Features
- Task 1 --- Text transformation: summarize, translate, or change
  the tone of supplied text.
- Task 2 --- Resume parsing: extract structured resume information
  from text or an uploaded PDF.
- Task 3 --- Question routing: classify a question as coding,
  math, or general, then send it to the corresponding prompt chain.
- Task 4 --- Social content generation: generate a tweet, LinkedIn
  caption, and hashtags for a topic in parallel.
- Task 5 --- Safe JSON generation: ask the model for JSON and
  attempt to repair the response if it is invalid.
- Health endpoint: a lightweight endpoint for checking whether the
  API is running.
Project structure
LangChain-Testing-main/
├── LLMs/
│   ├── __init__.py
│   └── base.py                 # Shared OpenRouter ChatOpenAI client
├── Prompts/
│   ├── summary.txt
│   ├── translate.txt
│   ├── tone.txt
│   ├── resume_parser.txt
│   ├── Task-3/
│   │   ├── coding.txt
│   │   ├── math.txt
│   │   └── general.txt
│   ├── Task-4/
│   │   ├── tweet.txt
│   │   ├── linkedin.txt
│   │   └── hashtags.txt
│   └── Task-5/
│       └── safe_json.txt
├── Task1/                      # Text transformation
├── Task2/                      # Resume parsing
├── Task3/                      # Question classification and routing
├── Task4/                      # Social content generation
├── Task5/                      # JSON generation and repair
├── util/
│   └── pdf.py                  # PDF text extraction
├── config.py                   # Environment-backed settings
├── main.py                     # FastAPI application and router registration
├── requirements.txt
└── README.md

Requirements
- Python 3.10 or newer is recommended.
- An OpenRouter API key and a model identifier available to your
  account.
- A Hugging Face access token and model identifier for the settings
  currently declared in config.py.
- Internet access for calls to hosted models.
The application currently creates its shared chat model in
LLMs/base.py using the OpenRouter-compatible API. The Hugging Face
settings are declared in config.py, but are not used by that shared
client in the code reviewed here.

Setup
1. Open the project folder
Open the extracted LangChain-Testing-main folder in VS Code, then open
a terminal in that folder.
2. Create and activate a virtual environment
Windows PowerShell:
py -m venv .venv
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, you can run the environment's Python
directly with .\.venv\Scripts\python.exe.
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install fastapi "uvicorn[standard]" pydantic-settings pypdf python-multipart
The additional packages cover imports and PDF upload handling used by
the application. If a package is already installed, pip will leave it
available.
4. Configure environment variables
Create a file named .env in the project root, next to config.py. Add
your own credentials and model identifiers:
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_POOLSIDE_MODEL=your_openrouter_model_identifier
OPENROUTER_GEMMA_MODEL=your_openrouter_model_identifier
HUGGINGFACEHUB_ACCESS_TOKEN=your_hugging_face_token
HUGGINGFACE_FASTCONTEXT_MODEL=your_hugging_face_model_identifier
EMBEDDING_MODEL=your_embedding_model_identifier
TEMPERATURE=0.8
Use actual model IDs supported by your providers. LLMs/base.py
currently uses OPENROUTER_GEMMA_MODEL, OPENROUTER_API_KEY, and
TEMPERATURE.

Security: never commit .env or paste API keys into source code,
screenshots, or public repositories. If a real key has been exposed,
revoke it with the provider and create a replacement. The repository's
.gitignore already excludes .env.
5. Start the API
From the project root, run:
uvicorn main:app --reload
The development server should be available at http://127.0.0.1:8000.
- Interactive Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health
The --reload option is intended for local development, not production
deployment.
API endpoints
All routes are registered in main.py. The request and response schemas
are defined in each task's schemas.py.
Health check
GET /health

Example response:
{
  "status": "ok"
}
Task 1 --- Text transformation
POST /transform

Accepts an action, input text, and an instruction. Supported action
values in the current chain are summarize, translate, and
tone-shift.

Example request:
{
  "action": "summarize",
  "text": "Paste the text you want to summarize here.",
  "instruction": "Summarize it in three concise bullet points."
}
The response contains a response string.
Task 2 --- Resume parsing
POST /parse-resume

Accepts resume text as JSON:
{
  "resume": "Paste the resume text here."
}
The response follows the ResumeResponse schema:
{
  "name": "Candidate Name",
  "skills": ["Python", "SQL"],
  "years_of_experience": 2,
  "last_role": "Software Engineer"
}
The values above are illustrative; actual output depends on the input
and model.

POST /parse-resume-file

Accepts a PDF file as multipart form data. Use the Swagger UI's file
picker or send a multipart request. The current implementation extracts
text from PDF pages before passing it to the resume parser;
scanned/image-only PDFs may need OCR, which is not implemented here.
Task 3 --- Question routing
POST /ask

Accepts a question and classifies it into coding, math, or
general, then invokes the corresponding prompt.

Example request:
{
  "question": "Explain the difference between a list and a tuple in Python."
}
The response contains the predicted category and the generated
answer.
Task 4 --- Social content generation
POST /generate-post

Example request:
{
  "topic": "Why learning Python is useful for beginners"
}
The response contains:
- tweet
- linkedin_caption
- hashtags (a list)
The three content chains are invoked in parallel.
Task 5 --- Safe JSON generation
POST /safe-json

Example request:
{
  "prompt": "Create a JSON object for a fictional book with title, author, and publication_year."
}
The response wraps the parsed JSON object in a data field. The current
implementation retries with a repair prompt if the first model response
cannot be parsed as JSON. This is a best-effort repair flow, not a
guarantee that every response will be valid or semantically correct.
Testing the API
1. Start the server with uvicorn main:app --reload.
2. Open http://127.0.0.1:8000/docs.
3. Expand an endpoint and select Try it out.
4. Enter the JSON request body, or choose a PDF for
   /parse-resume-file.
5. Select Execute and inspect the response and HTTP status code.
You can also test the health endpoint in a browser at
http://127.0.0.1:8000/health.
Implementation notes and limitations
- Prompt files are read from the repository's Prompts/ directory.
  Run the API from the project root so relative paths used by Task 1
  and Task 2 resolve correctly.
- Task 3, Task 4, and Task 5 build their prompt paths relative to
  their Python files.
- Model responses can be inaccurate. Validate generated resume fields
  and JSON before using them for consequential decisions.
- The PDF parser extracts selectable text; OCR for scanned PDFs is not
  included.
- The current Task 5 response schema expects a JSON object (dict),
  not a top-level JSON array or scalar.
- The current Task 1 load_prompt() helper returns a tuple of prompt
  strings, as written in the source. If Task 1 behaves unexpectedly,
  review that helper and ensure each action receives the intended
  prompt.
- API calls require valid provider credentials and may incur provider
  usage charges.
Troubleshooting
ValidationError when starting the app
Check that .env exists in the project root and that all required
settings declared in config.py are present. Confirm there are no
accidental spaces around variable names.

ModuleNotFoundError
Activate the project's virtual environment and install dependencies
using the commands above. Make sure VS Code is using the same
interpreter.

Provider authentication or model errors
Verify OPENROUTER_API_KEY and OPENROUTER_GEMMA_MODEL, and check that
the model ID is available to your OpenRouter account.

/parse-resume-file fails on upload
Ensure python-multipart is installed and that the uploaded file is a
valid PDF. The endpoint currently expects a PDF, not DOCX.

Prompt file not found
Run uvicorn main:app --reload from the project root, or update the
relevant code to use paths relative to the source file.
License
No license file was present in the supplied project archive. Add a
LICENSE file if you intend to publish or distribute the project, and
choose a license that fits your intended use.
