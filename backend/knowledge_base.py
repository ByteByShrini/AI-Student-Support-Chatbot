import os
import pickle
import pandas as pd

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer


# --------------------------------
# Paths
# --------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DOCUMENT_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "documents"
)

FAQ_PATH = os.path.join(
    BASE_DIR,
    "data",
    "faqs.csv"
)

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "knowledge_base.pkl"
)


# --------------------------------
# Read FAQ data
# --------------------------------

def load_faqs():

    faqs = pd.read_csv(
        FAQ_PATH
    )

    chunks = []

    for _, row in faqs.iterrows():

        question = str(
            row["question"]
        )

        answer = str(
            row["answer"]
        )

        chunks.append({

            "source": "FAQ",

            "text": (
                f"Question: {question}\n"
                f"Answer: {answer}"
            )

        })

    return chunks


# --------------------------------
# Read PDF documents
# --------------------------------

def load_pdfs():

    chunks = []

    for filename in os.listdir(
        DOCUMENT_FOLDER
    ):

        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        reader = PdfReader(
            file_path
        )

        full_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                full_text += text + "\n"

        # Split into chunks

        words = full_text.split()

        chunk_size = 500
        overlap = 50

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_text = " ".join(
                words[start:end]
            )

            if chunk_text.strip():

                chunks.append({

                    "source": filename,

                    "text": chunk_text

                })

            start += (
                chunk_size - overlap
            )

    return chunks


# --------------------------------
# Build knowledge base
# --------------------------------

def build_knowledge_base():

    print(
        "Loading FAQ data..."
    )

    faq_chunks = load_faqs()

    print(
        f"FAQ chunks: {len(faq_chunks)}"
    )

    print(
        "Loading PDF documents..."
    )

    pdf_chunks = load_pdfs()

    print(
        f"PDF chunks: {len(pdf_chunks)}"
    )

    all_chunks = (
        faq_chunks +
        pdf_chunks
    )

    return all_chunks


# --------------------------------
# Create TF-IDF vectors
# --------------------------------

def create_embeddings(chunks):

    print(
        "\nCreating TF-IDF vectors..."
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    embeddings = vectorizer.fit_transform(
        texts
    )

    return vectorizer, embeddings


# --------------------------------
# Main
# --------------------------------

if __name__ == "__main__":

    print(
        "Building knowledge base..."
    )

    chunks = build_knowledge_base()

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    if len(chunks) == 0:

        print(
            "No FAQ or PDF data found."
        )

        exit()

    vectorizer, embeddings = create_embeddings(
        chunks
    )

    knowledge_base = {

        "chunks": chunks,

        "vectorizer": vectorizer,

        "embeddings": embeddings

    }

    with open(
        OUTPUT_PATH,
        "wb"
    ) as file:

        pickle.dump(
            knowledge_base,
            file
        )

    print(
        "\nKnowledge base created successfully!"
    )

    print(
        f"Embeddings shape: {embeddings.shape}"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )