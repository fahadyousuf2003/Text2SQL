from flask import Flask, request, jsonify
from text2sql import setup_database_and_llm, create_query_chain

app = Flask(__name__)

# Initialize database and LLM
try:
    db, llm = setup_database_and_llm()
    process_question = create_query_chain(llm, db)
except Exception as e:
    raise RuntimeError(f"Failed to initialize services: {str(e)}")

@app.route('/ask', methods=['POST'])
def ask_question():
    """API endpoint to handle text-to-SQL queries."""
    try:
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        # Process the question using the query chain
        response = process_question(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
