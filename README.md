AI Task API for Softvence Omega (Betopia Group) - Candidate Submission
Overview
This project implements a FastAPI API with a single /ai-task route to handle four tasks as per the recruitment requirements:

Q&A: Agent-based question answering using a local LLM (Ollama) with free tools (DuckDuckGo for search, yfinance for stock data).
Fetch Latest Answer: Retrieves the most recent Q&A response.
Image Generation: Generates images using the free HuggingFace Inference API (Stable Diffusion).
Content Generation: Tailors content for platforms (Facebook, LinkedIn, Twitter, Instagram) using local LLM.


Authentication: Optional JWT with indefinite validity.
MCP Integration: Simulated using langgraph for local agent control, mimicking the reference code’s MCP setup.
Backtest: Moving Average Crossover strategy for trading, with CSV, chart, and metrics outputs.

Folder Structure

app.py: FastAPI backend with /ai-task route and JWT auth.
frontend.py: Streamlit frontend for user interaction.
models.py: Pydantic models for request validation.
utils.py: Helper functions for agent, content, and image generation.
backtest.py: Backtest script for trading strategy.
backtest/: Outputs (CSV, chart, metrics).
.env: Environment variables (HF_TOKEN, SECRET_KEY).
requirements.txt: Dependencies.
Dockerfile: Docker configuration for Render deployment.
render.yaml: Render deployment configuration.

Setup Instructions

Install Dependencies:
pip install -r requirements.txt

Dependencies: fastapi, uvicorn, streamlit, pydantic, langchain, langgraph, langchain-community, huggingface-hub, yfinance, matplotlib, numpy, python-dotenv, python-jose.

Set Up Ollama:

Install Ollama: ollama.ai.
Run: ollama run llama3.2.


Set Up HuggingFace Token:

Get a free API token: huggingface.co/settings/tokens.
Create .env in project root:HF_TOKEN=your_huggingface_token
SECRET_KEY=your_secret_key_here




Run Backend Locally:
python app.py


Run Frontend Locally:
streamlit run frontend.py


Run Backtest:
python backtest.py

Outputs: backtest/backtest_results.csv, backtest/backtest_chart.png, backtest/metrics.txt.


Deployment on Render

Push to GitHub:

Create a repository: [e.g., github.com/yourusername/ai-task-project].
Push all files (except .env).

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ai-task-project.git
git push -u origin main


Set Up Render:

Sign up for Render’s free tier: render.com.
Create a new web service, selecting your GitHub repo.
Use the render.yaml configuration or manually set:
Environment: Docker
Region: Oregon (or other free tier region)
Plan: Free
Branch: main


Add environment variables in Render dashboard:
HF_TOKEN: Your HuggingFace API token.
SECRET_KEY: Your JWT secret key.


Deploy: Render will build the Dockerfile and start the service.


Frontend Deployment:

Deploy frontend.py on Streamlit Sharing: streamlit.io/cloud.
Update BACKEND_URL in frontend.py to your Render URL (e.g., https://ai-task-api.onrender.com/ai-task).
Push to a separate GitHub repo for Streamlit and deploy.


Demo Link:

Backend: [e.g., https://ai-task-api.onrender.com] (update after deployment).
Frontend: [e.g., https://your-streamlit-app.streamlit.app] (update after deployment).



Usage

Frontend: Use Streamlit to select tasks, input prompts, and provide JWT (optional).
Backend: POST to /ai-task (e.g., https://ai-task-api.onrender.com/ai-task):{
  "task": "qa",
  "prompt": "Should I invest in Tesla?",
  "platform": null
}

For content generation, specify platform (e.g., "Twitter").
JWT: Generate via /generate-token endpoint (e.g., https://ai-task-api.onrender.com/generate-token).

Backtest Details

Strategy: MA50 > MA200 (buy), MA50 < MA200 (sell) on AAPL (2020-01-01 to 2025-08-14).
Outputs:
backtest_results.csv: Historical data with signals/returns.
backtest_chart.png: Cumulative return plot.
metrics.txt: Total return, Sharpe ratio.


Risk Controls: MA signals reduce overfitting; recommend stop-loss (e.g., 5%) for real trading.
Assumptions: No slippage/commissions; yfinance data is reliable; historical results not predictive.

Approach, Risk Controls, and Assumptions

Approach: Used free tools (Ollama for Q&A/content, HuggingFace for images, yfinance for trading data). Agent uses langgraph to simulate MCP’s tool-calling. Content tailored via platform-specific prompts. Backtest uses MA crossover, with Q&A supporting trading queries.
Risk Controls: Backtest uses MA signals; real trading needs stop-losses and position sizing. Agent responses are informational.
Assumptions: Local LLM (llama3.2) is sufficient. HuggingFace API is free with token. Historical data from yfinance is accurate.

Submission

GitHub: [e.g., github.com/yourusername/ai-task-project] (update after pushing).
Demo Link: [e.g., https://ai-task-api.onrender.com] (update after deployment).
JWT Token: Generate via /generate-token.
Form: Submit via Google Form by August 17, 2025, 23:59 UTC+6.
Contact: roksana18cse04@gmail.com.

Submitted by [Your Name], August 16, 2025.
