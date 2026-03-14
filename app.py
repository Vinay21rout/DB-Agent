import streamlit as st
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from sqlalchemy import create_engine
from dotenv import load_dotenv
from typing import TypedDict
import os
from langchain_community.utilities import SQLDatabase
from urllib.parse import quote_plus

load_dotenv()

# Page config
st.set_page_config(
    page_title="DB Agent Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# State definition
class SqlAgentState(TypedDict):
    database: str
    db_uri: str
    db: SQLDatabase
    question: str
    sql_query: str
    sql_response: str
    final_answer: str
    schema: str

# Agent functions
def db_selector(state: SqlAgentState):
    DB_SELECTOR_PROMPT = f"""
You are an intelligent database router.

Your task is to select the correct database that contains the data needed to answer the user's question.

Available Databases:

Database: school
Tables:
students(student_id, name, department)
courses(course_id, course_name)
enrollments(student_id, course_id)

Database: company
Tables:
employees(emp_id, name, salary)
departments(dept_id, dept_name)
transactions(transaction_id, amount)

Rules:
- Select the MOST relevant database.
- Return ONLY the database name.
- Do not explain your reasoning.

User Question:
{state["question"]}

Return only one database name.
"""
    response = llm.invoke(DB_SELECTOR_PROMPT)
    return {"database": response.content.strip()}

def connection_evaluator(state: SqlAgentState):
    uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{state['database']}"
    try:
        db = SQLDatabase.from_uri(uri)
        schema = db.get_table_info()
        return {"db_uri": uri, "db": db, "schema": schema}
    except Exception as e:
        st.error(f"Connection failed: {e}")
        raise

def generate_sql_query(state: SqlAgentState):
    GENERATE_SQL_QUERY_PROMPT = f"""
You are a senior SQL engineer.

Your job is to convert the user question into a SQL query.

Database Schema:
{state["schema"]}

Rules:
- Use only the tables and columns present in the schema.
- Do not hallucinate tables.
- Return ONLY SQL.
- Do not add explanations.

User Question:
{state["question"]}

SQL Query:
"""
    response = llm.invoke(GENERATE_SQL_QUERY_PROMPT)
    return {"sql_query": response.content.replace("```","").strip("sql")}

def generate_sql_response(state: SqlAgentState):
    db_response = state['db'].run(state['sql_query'])
    return {"sql_response": db_response}

def execute(state: SqlAgentState):
    FINAL_RESPONSE_PROMPT = f"""
You are a data analyst.

A SQL query was executed to answer a user's question.

User Question:
{state["question"]}

SQL Query:
{state["sql_query"]}

SQL Result:
{state["sql_response"]}

Explain the result clearly in natural language.

Rules:
- Provide a clear answer
- If result is empty, say no data was found
- Do not show SQL unless necessary
"""
    response = llm.invoke(FINAL_RESPONSE_PROMPT)
    return {"final_answer": response.content}

# Build workflow
@st.cache_resource
def build_workflow():
    graph = StateGraph(SqlAgentState)
    
    graph.add_node("db_selector", db_selector)
    graph.add_node("connection_evaluator", connection_evaluator)
    graph.add_node("generate_sql_query", generate_sql_query)
    graph.add_node("generate_sql_response", generate_sql_response)
    graph.add_node("execute", execute)
    
    graph.add_edge(START, "db_selector")
    graph.add_edge("db_selector", "connection_evaluator")
    graph.add_edge("connection_evaluator", "generate_sql_query")
    graph.add_edge("generate_sql_query", "generate_sql_response")
    graph.add_edge("generate_sql_response", "execute")
    graph.add_edge("execute", END)
    
    return graph.compile()

workflow = build_workflow()

# UI
st.title("🤖 DB Agent Chatbot")
st.markdown("Ask questions about your databases in natural language!")

# Sidebar
with st.sidebar:
    st.header("📊 Available Databases")
    st.markdown("""
    **School Database:**
    - students
    - courses
    - enrollments
    
    **Company Database:**
    - employees
    - departments
    - transactions
    """)
    
    st.divider()
    
    st.markdown("### 💡 Example Questions")
    examples = [
        "How many students are in Computer Science?",
        "What is the average salary of employees?",
        "List all courses",
        "Show me all departments"
    ]
    
    for example in examples:
        if st.button(example, key=example):
            st.session_state.messages.append({"role": "user", "content": example})
            with st.spinner("Processing..."):
                result = workflow.invoke({"question": example})
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["final_answer"],
                    "sql": result.get("sql_query", ""),
                    "database": result.get("database", "")
                })
            st.rerun()

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sql" in message:
            with st.expander("🔍 View SQL Query"):
                st.code(message["sql"], language="sql")
            if "database" in message:
                st.caption(f"📁 Database: `{message['database']}`")

# Chat input
if prompt := st.chat_input("Ask a question about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = workflow.invoke({"question": prompt})
                
                st.markdown(result["final_answer"])
                
                with st.expander("🔍 View SQL Query"):
                    st.code(result["sql_query"], language="sql")
                
                st.caption(f"📁 Database: `{result['database']}`")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["final_answer"],
                    "sql": result["sql_query"],
                    "database": result["database"]
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
