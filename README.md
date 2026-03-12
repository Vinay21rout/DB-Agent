# SQL Agent Chatbot 🤖

An intelligent SQL agent that automatically selects the appropriate database, generates SQL queries, and provides natural language responses to user questions using LangGraph and LLM.

## 🌟 Features

- **Intelligent Database Selection**: Automatically routes queries to the correct database based on user questions
- **Natural Language to SQL**: Converts user questions into optimized SQL queries
- **Multi-Database Support**: Currently supports `school` and `company` databases
- **Natural Language Responses**: Converts SQL results into human-readable answers
- **Built with LangGraph**: Implements a state-based workflow for reliable query processing

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
git clone <your-repo-url>
cd agentic_project
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

### Using Jupyter Notebook

Open and run `chatbot.ipynb`:
```bash
jupyter notebook chatbot.ipynb
```

### Example Queries

```python
# Initialize the workflow
result = workflow.invoke({
    "question": "How many students are enrolled in Computer Science?"
})
print(result["final_answer"])
```

**Sample Questions:**
- "List all students in the Computer Science department"
- "What is the average salary of employees?"
- "Show me all courses"
- "How many transactions were made?"

## 🏗️ Architecture

The agent follows a 5-step workflow:

1. **DB Selector**: Identifies the relevant database
2. **Connection Evaluator**: Establishes database connection and retrieves schema
3. **Generate SQL Query**: Converts natural language to SQL
4. **Generate SQL Response**: Executes the query
5. **Execute**: Formats results into natural language

## 📁 Project Structure

```
agentic_project/
├── chatbot.ipynb          # Main Jupyter notebook
├── main.py                # Python script version (if applicable)
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not tracked)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔜 Coming Soon

- **Web UI**: Interactive web interface for easier interaction (Under Development)
- Additional database support
- Query history and caching
- Advanced error handling
- Export results to CSV/JSON

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Known Issues

- Ensure database credentials are correctly set in `.env`
- Complex queries may require schema optimization

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: UI interface is currently under development and will be added soon! 🚧
