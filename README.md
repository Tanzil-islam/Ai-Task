
# AI Trader Task API

A **FastAPI-based multi-task AI API** built for **Softvence Omega recruitment**.
This project demonstrates integrating multiple AI services (Q\&A, Image Generation, Content Generation) into a single API endpoint with optional **JWT authentication** and **MCP (Model Context Protocol) client/server integration**.

---

## 🚀 Features

* **Unified API Endpoint (`/ai-task`)** for:

  * **Q\&A (Agent-based)** – ask questions and save answers to the database.
  * **Fetch Latest** – retrieve the latest Q\&A entry.
  * **Generate Image** – create AI-generated images from text prompts.
  * **Generate Platform-Specific Content** – tailored for Facebook, LinkedIn, Twitter, Instagram, etc.

* **JWT Authentication** (`/token`) – optional but supported.

* **Database Support** – SQLite with async `aiosqlite`.

* **MCP Client/Server Integration** – simulated tools for text generation, image analysis, and content optimization.

* **Frontend Hosting** – serves static files from `/frontend`.

* **Health Check** (`/health`) – verify service status.

---

## 🗂️ Project Structure

```
├── main.py                # FastAPI app with all routes
├── models.py              # Request/Response models
├── auth.py                # JWT creation & verification
├── database.py            # Async SQLite database operations
├── services/
│   ├── qa_service.py      # Q&A handling
│   ├── image_service.py   # AI-based image generation
│   ├── content_service.py # Social media content generation
├── mcp_client.py          # MCP client & server simulation
├── frontend/              # Static frontend files
├── .env                   # API keys & environment variables
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/Tanzil-islam/Ai-Task.git
   cd Ai-Task
   ```

2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set environment variables** (create a `.env` file):

   ```
   OPENAI_API_KEY=your_openai_key
   REPLICATE_API_KEY=your_replicate_key
   HUGGINGFACE_API_KEY=your_huggingface_key
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=your_secret_key
   ```

4. **Run the app**

   ```bash
   uvicorn main:app --reload
   ```

   Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger API docs.

---

## 📌 Usage

### 1. Authentication (optional)

```http
POST /token
{
  "username": "admin",
  "password": "password"
}
```

### 2. AI Tasks (`/ai-task`)

```http
POST /ai-task
{
  "task": "qa",
  "question": "What is AI?"
}
```

Supported tasks:

* `qa` – Q\&A with DB storage
* `fetch_latest` – fetch latest Q\&A entry
* `generate_image` – generate image from `prompt`
* `generate_content` – generate social media content from `prompt`

Example for content generation:

```http
POST /ai-task
{
  "task": "generate_content",
  "prompt": "AI in finance",
  "platform": "linkedin"
}
```

---

## 🔧 MCP Integration

The project includes a **simplified MCP client/server** for tool simulation:

* `text_generation`
* `image_analysis`
* `content_optimization`

These are used internally for fallback AI operations.

---

## 🗄️ Database

* **SQLite** is used by default.
* Stores all Q\&A interactions with timestamp.
* Auto-creates `qa_entries` table on startup.

---


## 📊 Deliverables

* FastAPI multi-task AI API
* JWT authentication
* MCP integration
* Database logging of Q\&A
* AI-based content & image generation
* Frontend static file hosting

---


