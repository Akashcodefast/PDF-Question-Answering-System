from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from utils.pdf_loader import load_pdf_text
from utils.text_splitter import split_text
from utils.embeddings import create_vector_store
from utils.qa_chain import get_conversational_chain

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_pdf():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    temp_path = "temp.pdf"
    file.save(temp_path)

    raw_text = load_pdf_text(temp_path)

    text_chunks = split_text(raw_text)

    create_vector_store(text_chunks)

    return jsonify({
        "message": "PDF processed successfully"
    })

@app.route('/ask', methods=['POST'])
def ask_question():

    data = request.json

    question = data.get('question')

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question)

    chain = get_conversational_chain()

    response = chain(
        {
            "input_documents": docs,
            "question": question
        },
        return_only_outputs=True
    )

    return jsonify({
        "answer": response["output_text"]
    })


if __name__ == '__main__':
    app.run(debug=True)