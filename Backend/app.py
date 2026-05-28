from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.pdf_loader import load_pdf_text
from utils.text_splitter import split_text
from utils.embeddings import create_vector_store

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "PDF Question Answering Backend Running"


@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "No file selected"
            }), 400

        print("PDF upload started")

        temp_path = "temp.pdf"

        file.save(temp_path)

        print("PDF saved")

        raw_text = load_pdf_text(temp_path)

        print("PDF text extracted")

        if not raw_text.strip():
            return jsonify({
                "error": "No readable text found in PDF"
            }), 400

        text_chunks = split_text(raw_text)

        print("Chunks created")

        create_vector_store(text_chunks)      

        print("Vector store created")

        return jsonify({
            "message": "PDF processed successfully"
        })

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/ask", methods=["POST"])
def ask_question():

    try:

        data = request.json

        question = data.get("question")

        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400

        print("Question received")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        db = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )

        print("Vector store loaded")

        docs = db.similarity_search(question)

        print("Similarity search completed")

        answer = ""

        for doc in docs:
            answer += doc.page_content + "\n\n"

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("QUESTION ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)