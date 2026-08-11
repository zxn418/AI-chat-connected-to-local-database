# AI Query Assistant 🤖

A Streamlit app that lets you ask natural-language questions about your SQL Server data, powered by [PandasAI](https://github.com/sinaptik-ai/pandas-ai) and OpenAI's GPT-4o.

Ask things like *"what are healthy foods and unhealthy foods and the quantity of each"* and get back tables, numbers, text, or auto-generated charts — no SQL required.

---

## ✨ Features

- 🔌 Connects directly to a SQL Server database via `pyodbc`
- 🧠 Uses PandasAI + LiteLLM to turn plain-English questions into data analysis
- 📊 Renders responses as tables, numbers, text, or charts automatically
- 💬 Simple chat interface built with Streamlit

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web app UI |
| [PandasAI](https://github.com/sinaptik-ai/pandas-ai) | Natural-language data analysis |
| [LiteLLM](https://github.com/BerriAI/litellm) | LLM provider integration |
| [pyodbc](https://github.com/mkleehammer/pyodbc) | SQL Server connectivity |
| [uv](https://github.com/astral-sh/uv) | Python package & environment management |

---

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.11** (this project does *not* support 3.12+)
- **[uv](https://docs.astral.sh/uv/)** installed
- **ODBC Driver 18 for SQL Server** installed on your machine
- Access to a SQL Server database
- An **OpenAI API key**

Check your ODBC driver is installed:
```bash
uv run python -c "import pyodbc; print(pyodbc.drivers())"
```
You should see `'ODBC Driver 18 for SQL Server'` in the output list.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ai-con-database
```

### 2. Pin Python version and install dependencies
```bash
uv python install 3.11
uv python pin 3.11
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-key-here

DB_SERVER=your-sql-server-address
DB_DATABASE=your-database-name
DB_USERNAME=your-db-username
DB_PASSWORD=your-db-password
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

### 4. Run the app
```bash
uv run streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
ai-con-database/
├── main.py             # Streamlit app entry point
├── pyproject.toml      # Project dependencies
├── .env                # Environment variables (not committed)
├── .python-version     # Pinned Python version
└── README.md
```

---

## ⚙️ How It Works

```
pyodbc  →  SQL Server (view/table)  →  DataFrame  →  PandasAI Agent  →  Response  →  Streamlit UI
```

1. `pyodbc` connects to SQL Server and runs a query
2. The result is loaded into a pandas `DataFrame`
3. The DataFrame is wrapped in `pai.DataFrame(...)` with metadata so PandasAI understands the data
4. A PandasAI `Agent` is created and handles user questions via `agent.chat(...)`
5. Responses are rendered in Streamlit as a table, number, text, or chart depending on type
