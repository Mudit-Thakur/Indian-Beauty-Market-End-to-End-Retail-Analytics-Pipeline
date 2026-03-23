# ============================================================
# Indian Beauty Market - AI Analytics Agent v2.0
# Natural Language to SQL using LangChain + Groq + DuckDB
# Upgrades: Plain English answers + Memory + Chat History Log
# ============================================================

import duckdb
import os
import json
from datetime import datetime
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# STEP 1 — CONFIGURATION
# ============================================================

GROQ_API_KEY = "please put your grok API key here" #<--- visit console.grok.ai click on apui key to get yours today

DATA_PATH = r"your data path" #<--- change this to your data path

LOG_PATH = r"your log path" #<--- change this to your log path

# ============================================================
# STEP 2 — CONNECT TO DUCKDB AND LOAD PARQUET FILES
# ============================================================

con = duckdb.connect()

con.execute(f"CREATE VIEW sales AS SELECT * FROM read_parquet('{DATA_PATH}/sales_cleaned.parquet')")
con.execute(f"CREATE VIEW customer_rfm AS SELECT * FROM read_parquet('{DATA_PATH}/customer_rfm.parquet')")
con.execute(f"CREATE VIEW product_performance AS SELECT * FROM read_parquet('{DATA_PATH}/product_performance.parquet')")
con.execute(f"CREATE VIEW festival_sales AS SELECT * FROM read_parquet('{DATA_PATH}/festival_sales.parquet')")
con.execute(f"CREATE VIEW city_performance AS SELECT * FROM read_parquet('{DATA_PATH}/city_performance.parquet')")
con.execute(f"CREATE VIEW monthly_sales AS SELECT * FROM read_parquet('{DATA_PATH}/monthly_sales.parquet')")
con.execute(f"CREATE VIEW customer_metrics AS SELECT * FROM read_parquet('{DATA_PATH}/customer_level_metrics.parquet')")

print("✅ Database connected. All tables loaded.")

# ============================================================
# STEP 3 — INITIALIZE GROQ LLM
# ============================================================

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# ============================================================
# STEP 4 — CONVERSATION MEMORY
# Stores last 5 questions and answers
# So agent remembers context between questions
# Like a human analyst who remembers what you just asked
# ============================================================

conversation_memory = []
MAX_MEMORY = 5

def update_memory(question, sql, answer_summary):
    """Add latest exchange to memory. Keep only last 5."""
    conversation_memory.append({
        "question": question,
        "sql": sql,
        "answer": answer_summary
    })
    # Keep only last MAX_MEMORY exchanges
    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory.pop(0)

def get_memory_context():
    """Format memory into a string for the AI prompt."""
    if not conversation_memory:
        return "No previous questions in this session."
    
    context = "Previous questions in this session:\n"
    for i, exchange in enumerate(conversation_memory, 1):
        context += f"{i}. Q: {exchange['question']}\n"
        context += f"   A: {exchange['answer']}\n"
    return context

# ============================================================
# STEP 5 — DATABASE SCHEMA
# ============================================================

SCHEMA = """
You are an expert SQL analyst for an Indian beauty retail company.
You have access to these DuckDB tables:

1. sales (main transactions table)
   - transaction_id, customer_id, product_id, purchase_date
   - festival (Diwali/Holi/Summer/null), city
   - product_name, category, customer_name
   - age, gender, price, revenue

2. customer_rfm (customer segments)
   - customer_id, last_purchase, recency, frequency, monetary
   - r_score, f_score, m_score, rfm_score
   - segment (Champions/Loyal Customers/Potential Loyalists/At Risk)

3. product_performance (product analytics)
   - product_id, product_name, category
   - transactions, total_revenue, avg_price
   - revenue_share_pct, cumulative_revenue_pct

4. festival_sales (festival analytics)
   - festival, transactions, total_revenue
   - avg_order_value, revenue_share_pct

5. city_performance (geographic analytics)
   - city, transactions, total_revenue
   - average_order_value, revenue_share_pct

6. monthly_sales (time series)
   - year_month, transactions, total_revenue
   - average_order_value, revenue_share_pct

7. customer_metrics (customer KPIs)
   - customer_id, total_orders, total_spent
   - avg_order_value, first_purchase, last_purchase
   - customer_lifetime_days, purchase_frequency
   - customer_type (VIP/Loyal/Regular/Low Value)

RULES:
- Write DuckDB compatible SQL only
- Always use LIMIT 10 unless user asks for more
- Return ONLY the SQL query — no explanation, no markdown, no backticks
- Revenue is in Indian Rupees
- Use revenue or total_revenue for revenue questions
"""

# ============================================================
# STEP 6 — PROMPTS
# Two prompts:
# Prompt 1 — converts question to SQL
# Prompt 2 — converts SQL results to plain English explanation
# ============================================================

# Prompt 1 — SQL Generation
# Takes question + memory context → returns SQL query
sql_prompt = ChatPromptTemplate.from_messages([
    ("system", SCHEMA + "\n\nContext from previous questions:\n{memory}"),
    ("human", "Convert this question to SQL: {question}")
])

# Prompt 2 — Plain English Explanation
# Takes question + SQL results → returns human readable answer
explanation_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly data analyst explaining results to a business stakeholder.
    Given a question and the SQL query results, provide:
    1. A direct answer to the question in 1-2 sentences
    2. One key business insight or recommendation
    Keep it concise and business focused.
    Use Indian Rupee (Rs.) for currency values."""),
    ("human", """Question: {question}
    
    Data Results:
    {results}
    
    Provide a clear business explanation.""")
])

# ============================================================
# STEP 7 — CHAT HISTORY LOG
# Saves every conversation to a text file
# So you can review past sessions
# Like keeping a journal of all your data queries
# ============================================================

def save_to_log(question, sql, results_str, explanation):
    """Save each exchange to chat history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'='*60}
Timestamp: {timestamp}
Question: {question}
SQL: {sql}
Results: {results_str}
Explanation: {explanation}
{'='*60}
"""
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)

# ============================================================
# STEP 8 — MAIN ASK FUNCTION
# Full pipeline:
# Question → Memory Context → SQL → DuckDB → Results → Explanation → Log
# ============================================================

def ask(question):
    """
    Full pipeline:
    1. Get memory context from previous questions
    2. Send question + memory to AI → get SQL
    3. Run SQL on DuckDB → get results
    4. Send results to AI → get plain English explanation
    5. Update memory with this exchange
    6. Save to chat log file
    """
    print(f"\n🔍 Question: {question}")
    print("-" * 60)
    
    try:
        # ---- Part A: Generate SQL with memory context ----
        # Memory makes follow-up questions work correctly
        memory_context = get_memory_context()
        
        sql_chain = sql_prompt | llm | StrOutputParser()
        sql_query = sql_chain.invoke({
            "question": question,
            "memory": memory_context
        })
        
        # Clean SQL output
        sql_query = sql_query.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        print(f"📝 SQL Generated:\n{sql_query}")
        print("-" * 60)
        
        # ---- Part B: Execute SQL on DuckDB ----
        result_df = con.execute(sql_query).fetchdf()
        
        if result_df.empty:
            print("⚠️  No results found.")
            return None
        
        # Convert results to string for display and AI explanation
        results_str = result_df.to_string(index=False)
        print(f"📊 Raw Results:\n{results_str}")
        print("-" * 60)
        
        # ---- Part C: Generate plain English explanation ----
        # This turns the table into a business insight
        explanation_chain = explanation_prompt | llm | StrOutputParser()
        explanation = explanation_chain.invoke({
            "question": question,
            "results": results_str
        })
        
        print(f"💡 Business Insight:\n{explanation}")
        
        # ---- Part D: Update conversation memory ----
        # Store short summary for context in next question
        summary = explanation[:200] if len(explanation) > 200 else explanation
        update_memory(question, sql_query, summary)
        
        # ---- Part E: Save to chat history log ----
        save_to_log(question, sql_query, results_str, explanation)
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try rephrasing your question.")
        return None

# ============================================================
# STEP 9 — INTERACTIVE CHAT LOOP
# ============================================================

def main():
    print("\n" + "="*60)
    print("🛍️  Indian Beauty Market — AI Analytics Agent v2.0")
    print("="*60)
    print("✨ Features: Natural Language → SQL → Business Insights")
    print("🧠 Memory: Remembers last 5 questions for context")
    print("📝 Logging: All conversations saved to chat_history.txt")
    print("\nType 'exit' to quit | Type 'memory' to see conversation history")
    print("\nExample questions:")
    print("  → Which city had the highest revenue?")
    print("  → Show top 5 products by revenue")
    print("  → How many at-risk customers do we have?")
    print("  → What was Diwali revenue?")
    print("  → Who are our VIP customers?")
    print("="*60 + "\n")
    
    # Create log file with session header
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n\n{'#'*60}\n")
        f.write(f"# NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'#'*60}\n")
    
    while True:
        question = input("💬 Ask a question: ").strip()
        
        if question.lower() in ['exit', 'quit', 'bye']:
            print("\n👋 Session ended. Chat saved to chat_history.txt")
            break
            
        if question.lower() == 'memory':
            print("\n🧠 Conversation Memory:")
            print(get_memory_context())
            continue
            
        if not question:
            continue
            
        ask(question)
        print()

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()