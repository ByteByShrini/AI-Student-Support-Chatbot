import os
from pypdf import PdfReader


DOCUMENT_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "documents"
)


def extract_text_from_pdfs():

    documents = []

    for filename in os.listdir(DOCUMENT_FOLDER):

        if filename.lower().endswith(".pdf"):

            file_path = os.path.join(
                DOCUMENT_FOLDER,
                filename
            )

            reader = PdfReader(file_path)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            documents.append({
                "filename": filename,
                "text": text
            })

    return documents


if __name__ == "__main__":

    documents = extract_text_from_pdfs()

    for document in documents:

        print("\n-------------------------")
        print("FILE:", document["filename"])
        print("-------------------------")

        print(
            document["text"][:2000]
        )