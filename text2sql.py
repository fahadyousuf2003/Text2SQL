import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

def setup_database_and_llm():
    """Initialize database connection and LLM"""
    # Get environment variables
    api_key = os.getenv('GROQ_API_KEY')
    db_url = os.getenv('DATABASE_URL')
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    # Initialize database
    db = SQLDatabase.from_uri(db_url)
    
    # Initialize LLM
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        verbose=True
    )
    
    return db, llm

def create_query_chain(llm, db):
    """Create the SQL query chain"""
    # Create template for SQL generation with more context
    sql_prompt = PromptTemplate.from_template("""
    Given the following database schema:
    {schema}
    
    Generate a SQL query to answer this question: {question}
    
    Return ONLY the SQL query without any additional text, markdown, or explanations.
    The query should be executable SQLite syntax.
    """)
    
    # Create template for final response
    response_prompt = PromptTemplate.from_template("""
    Question: {question}
    Generated SQL: {sql_query}
    Query Result: {result}
    
    Provide a natural language response that answers the question. If there was an error, explain it.
    """)

    def generate_sql(question):
        """Generate SQL query"""
        try:
            schema = db.get_table_info()
            context = {"schema": schema, "question": question}
            response = llm.invoke(sql_prompt.format(**context))
            sql_query = response.content.strip()
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            return sql_query
        except Exception as e:
            return f"Error generating SQL: {str(e)}"

    def execute_sql(sql_query):
        """Execute SQL query"""
        try:
            return db.run(sql_query)
        except Exception as e:
            return f"Error executing SQL: {str(e)}"

    def process_question(question):
        """Process the question and return response"""
        sql_query = generate_sql(question)
        result = execute_sql(sql_query)
        response = llm.invoke(
            response_prompt.format(
                question=question, sql_query=sql_query, result=result
            )
        )
        return response.content

    return process_question

def main():
    try:
        # Setup database and LLM
        db, llm = setup_database_and_llm()
        
        
        # Create the query chain
        process_question = create_query_chain(llm, db)
        
        # Interactive query loop
        while True:
            question = input("\nEnter your question (or 'quit' to exit): ")
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
                
            try:
                response = process_question(question)
                print("\nResponse:", response)
            except Exception as e:
                print(f"\nError processing question: {str(e)}")
                
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
