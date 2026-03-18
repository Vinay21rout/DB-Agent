# DB Agent 🤖

An intelligent SQL agent that automatically selects the appropriate database, generates SQL queries, and provides natural language responses to user questions — powered by LangGraph, LLM, and a Streamlit UI.

## 🌟 Features

- **Intelligent Database Selection**: Automatically routes queries to the correct database
- **Natural Language to SQL**: Converts user questions into optimized SQL queries
- **Multi-Database Support**: Supports `school` and `company` databases
- **Natural Language Responses**: Converts SQL results into human-readable answers
- **Interactive Web UI**: Clean Streamlit chat interface with SQL query viewer
- **SQL Safety Check**: Blocks dangerous queries containing DROP, DELETE, or TRUNCATE
- **Built with LangGraph**: State-based workflow for reliable query processing

## 📊 Supported Databases

### School Database
- `students` (student_id, name, department)
- `courses` (course_id, course_name)
- `enrollments` (student_id, course_id)

### Company Database
- `employees` (emp_id, name, salary)
- `departments` (dept_id, dept_name)
- `transactions` (transaction_id, amount)

## 🛠️ Tech Stack

- **LangChain & LangGraph**: Workflow orchestration
- **ChatGroq**: LLM provider (llama-3.3-70b-versatile)
- **Streamlit**: Web UI
- **SQLAlchemy**: Database connectivity
- **MySQL**: Database backend
- **Python 3.x**: Core language

## 📋 Prerequisites

- Python 3.8+
- MySQL database
- Groq API key
- LangSmith API key (optional, for tracing)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Vinay21rout/DB-Agent.git
cd DB-Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=DB_AGENT
```

## 💻 Usage

### Using Streamlit Web UI (Recommended)

Run the web interface:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**UI Features:**
- 💬 Interactive chat interface
- 🔍 Expandable SQL query viewer
- 📁 Shows which database was selected
- 💡 Quick example question buttons
- 🗑️ Clear chat history

### Using Jupyter Notebook (Backend Only)

To explore or test the backend logic directly:
```bash
jupyter notebook db_agent_backend_only.ipynb
```

```python
result = workflow.invoke({
    "question": "How many students are enrolled in Computer Science?"
})
print(result["final_answer"])
```

## 🏗️ Architecture

The agent follows a 5-step LangGraph workflow:

```
User Question
     ↓
DB Selector        → Identifies the relevant database (school / company)
     ↓
Connection Evaluator → Connects to DB and retrieves schema
     ↓
Generate SQL Query  → Converts natural language to SQL
     ↓
SQL Safety Check    → Blocks dangerous queries (DROP/DELETE/TRUNCATE)
     ↓
Generate SQL Response → Executes the SQL query
     ↓
Execute            → Returns a natural language answer
```

## 📁 Project Structure

```
DB-Agent/
├── app.py                        # Streamlit UI + Backend (main entry point)
├── db_agent_backend_only.ipynb   # Backend only - no UI (Jupyter notebook)
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (not tracked)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔜 Coming Soon

### 🧠 Agent Upgrades
- **Multi-Question Response**: Handle multiple questions in a single query and return combined answers
- **Smart Auto DB Selection**: Move beyond description-based routing — agent will intelligently detect the correct database using schema introspection and query context
- **Normal Chatbot Mode**: Agent will interact as a regular conversational chatbot when the question is not database-related, without triggering the SQL pipeline

### 🛠️ DB Connector as a Tool
- **Toggle On/Off Feature**: DB connection will be exposed as a switchable tool inside the agent — users can enable or disable database access directly from the UI
- When **ON**: Agent connects to the database and executes SQL queries
- When **OFF**: Agent operates as a normal conversational chatbot without any DB access

### 📦 General
- Additional database support
- Query history and caching
- Export results to CSV/JSON
- User authentication

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Known Issues

- Ensure database credentials are correctly set in `.env`
- Complex queries may require schema optimization

## 📧 Contact

For questions or suggestions, please open an issue on [GitHub](https://github.com/Vinay21rout/DB-Agent).

---

**Made with ❤️ using LangGraph and Streamlit**
