from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import pickle

from sklearn.metrics.pairwise import cosine_similarity


# ========================================
# CREATE FLASK APP
# ========================================

app = Flask(__name__)

CORS(app)


# ========================================
# LOAD KNOWLEDGE BASE
# ========================================

knowledge_base_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "knowledge_base.pkl"
)

with open(
    knowledge_base_path,
    "rb"
) as file:

    knowledge_base = pickle.load(file)


chunks = knowledge_base["chunks"]

vectorizer = knowledge_base["vectorizer"]

embeddings = knowledge_base["embeddings"]


# ========================================
# HOME ROUTE
# ========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "AI Student Support Chatbot API is running!"
    })


# ========================================
# CHAT ROUTE
# ========================================

@app.route("/chat", methods=["POST"])
def chat():

    # Get request data

    data = request.get_json()

    if not data:

        return jsonify({
            "answer": "Please provide a question."
        }), 400


    question = data.get(
        "question",
        ""
    ).strip()


    # Check empty question

    if not question:

        return jsonify({
            "answer": "Please enter a question."
        }), 400


    # ====================================
    # Convert question to TF-IDF vector
    # ====================================

    question_embedding = vectorizer.transform(
        [question]
    )


    # ====================================
    # Calculate similarity
    # ====================================

    similarities = cosine_similarity(
        question_embedding,
        embeddings
    )[0]


    # ====================================
    # Find best match
    # ====================================

    best_match_index = similarities.argmax()

    best_score = similarities[
        best_match_index
    ]


    # ====================================
    # Minimum similarity threshold
    # ====================================

    if best_score < 0.25:

        answer = (
            "Sorry, I could not find a relevant "
            "answer in the student support knowledge base."
        )

        source = "No relevant source"

    else:

        best_chunk = chunks[
            best_match_index
        ]

        text = best_chunk.get(
            "text",
            ""
        )

        source = best_chunk.get(
            "source",
            "Knowledge Base"
        )


        # =================================
        # Extract answer from FAQ format
        # =================================

        if "Answer:" in text:

            answer = text.split(
                "Answer:",
                1
            )[1].strip()

        else:

            answer = text.strip()


    # ====================================
    # Return response
    # ====================================

    return jsonify({

        "answer": answer,

        "source": source

    })


# ========================================
# RUN SERVER
# ========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )