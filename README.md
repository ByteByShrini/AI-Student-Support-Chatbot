# 🤖 AI Student Support Chatbot

An intelligent student support chatbot that helps students quickly find information about attendance, examinations, scholarships, fees, library services, hostel facilities, placements, internships, certificates, and other academic services.

The chatbot uses **Natural Language Processing (NLP)** and **semantic similarity search** to understand student questions and retrieve relevant answers from a structured FAQ dataset and PDF-based knowledge base.

---

## 📌 Project Overview

Students often need information about academic and administrative services, but finding the correct information can take time.

This project provides a simple conversational interface where students can ask questions in natural language and receive relevant answers from institutional information.

### Example

**Student:**

> How can I apply for a scholarship?

**Chatbot:**

> Students should check the official scholarship portal or institution notices for available scholarships, eligibility requirements, and application procedures.

---

## ✨ Features

- 💬 Natural-language student queries
- 📚 FAQ-based knowledge base
- 📄 PDF document knowledge base
- 🧠 Semantic similarity search
- 🔎 Relevant answer retrieval
- 🌐 Flask REST API
- 🖥️ Interactive web interface
- ⚡ Suggested questions
- ⏳ Typing/loading indicator
- 🧹 Clear chat functionality
- 🕐 Message timestamps
- 📄 Source information
- ❌ Unknown-question handling
- 📱 Responsive frontend

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask
- Flask-CORS

### AI / NLP

- Sentence Transformers
- Vector Embeddings
- Cosine Similarity
- Semantic Search

### Data Processing

- Pandas
- NumPy
- PyPDF2
- Pickle

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │     Student      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Web Frontend   │
                    │ HTML/CSS/JS       │
                    └────────┬─────────┘
                             │
                       HTTP POST
                             │
                             ▼
                    ┌──────────────────┐
                    │   Flask REST API │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Question         │
                    │ Embedding        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Semantic         │
                    │ Similarity Search│
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
             ┌──────────────┐   ┌──────────────┐
             │ FAQ Dataset  │   │ PDF Documents│
             └──────────────┘   └──────────────┘
                    │                  │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ Relevant Answer  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Student      │
                    └──────────────────┘
