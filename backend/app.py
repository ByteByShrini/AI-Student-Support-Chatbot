from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import pickle

from sentence_transformers import SentenceTransformer
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
    os.path.dirname(__file__),
    "knowledge_base.pkl"
)

with open(
    knowledge_base_path,
    "rb"
) as file:

    knowledge_base = pickle.load(file)


chunks = knowledge_base["chunks"]

embeddings = knowledge_base["embeddings"]


# ========================================
# LOAD EMBEDDING MODEL
# ========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ========================================
# HOME ROUTE
# ========================================

@app.route("/")
def home():

    return "AI Student Support Chatbot is running!"


# ========================================
# CHAT ROUTE
# ========================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    # Get request data

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()


    # ====================================
    # CHECK EMPTY QUESTION
    # ====================================

    if not question:

        return jsonify({
            "error": "Question is required"
        }), 400


    # ====================================
    # CREATE QUESTION EMBEDDING
    # ====================================

    question_embedding = model.encode(
        [question]
    )


    # ====================================
    # CALCULATE SIMILARITY
    # ====================================

    similarities = cosine_similarity(
        question_embedding,
        embeddings
    )[0]


    # ====================================
    # FIND BEST MATCH
    # ====================================

    best_match_index = similarities.argmax()

    best_score = similarities[
        best_match_index
    ]

    best_chunk = chunks[
        best_match_index
    ]


    # ====================================
    # DEBUG INFORMATION
    # ====================================

    print(
        "\nQuestion:",
        question
    )

    print(
        "Best similarity:",
        best_score
    )

    print(
        "Source:",
        best_chunk["source"]
    )


    # ====================================
    # GENERATE ANSWER
    # ====================================

    if best_score < 0.25:

        answer = (
            "Sorry, I couldn't find reliable "
            "information about that in the "
            "student support documents."
        )

        source = "No reliable source"


    else:

        answer = best_chunk["text"].strip()

        source = best_chunk["source"]


        # =================================
        # CLEAN FAQ RESPONSE
        # =================================

        if answer.startswith("Question:"):

            parts = answer.split(
                "Answer:",
                1
            )

            if len(parts) == 2:

                answer = parts[1].strip()


        # =================================
        # CLEAN COMMON Q/A FORMATS
        # =================================

        if answer.startswith("Q:"):

            if "A:" in answer:

                parts = answer.split(
                    "A:",
                    1
                )

                if len(parts) == 2:

                    answer = parts[1].strip()


        # =================================
        # REMOVE DUPLICATED QUESTION
        # =================================

        question_clean = (
            question
            .lower()
            .strip()
            .rstrip("?")
        )

        answer_lines = (
            answer.split("\n")
        )

        cleaned_lines = []


        for line in answer_lines:

            line_clean = (
                line
                .strip()
                .lower()
                .rstrip("?")
            )


            # Skip a line if it is
            # basically the user's question

            if line_clean == question_clean:

                continue


            cleaned_lines.append(
                line
            )


        answer = "\n".join(
            cleaned_lines
        ).strip()


    # ====================================
    # RETURN RESPONSE
    # ====================================

    return jsonify({

        "question": question,

        "answer": answer,

        "source": source,

        "similarity": round(
            float(best_score),
            2
        )

    })


# ========================================
# RUN SERVER
# ========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )