# CodeAlpha FAQ Chatbot

This is an NLP-based FAQ chatbot created for **CodeAlpha Artificial Intelligence Internship Task 2**.

It uses NLTK for preprocessing, TF-IDF for text representation, and cosine similarity for FAQ matching to return predefined answers. 

**Note: This is an NLP similarity matching bot, not an LLM chatbot.**

## Features

* Predefined dataset of 17 FAQs regarding Python and the CodeAlpha Internship.
* Natural Language Processing (NLP) pipeline to clean text.
* TF-IDF vectorization and Cosine Similarity calculation to match user queries with the most similar FAQ.
* Minimum similarity threshold (0.25) to reject completely unrelated questions.
* Clean, responsive HTML/CSS/Vanilla JS chat interface.
* Asynchronous backend communication (Fetch API).

## Technologies

* **Python 3.x**
* **Flask**: For the backend API endpoint (`/ask`).
* **NLTK**: For tokenization, stopword removal, and lemmatization.
* **scikit-learn**: For generating the TF-IDF matrix and calculating cosine similarity.
* **HTML/CSS/JavaScript**: Vanilla frontend implementation.

## Architecture

```text
User
 ↓
Web UI (Vanilla JS)
 ↓
Flask /ask endpoint (POST JSON)
 ↓
NLP preprocessing (NLTK)
 ↓
TF-IDF (scikit-learn)
 ↓
Cosine Similarity
 ↓
Best matching FAQ (Threshold applied)
 ↓
Predefined Answer
 ↓
Web UI (Chat message displayed)
```

## How NLP works in this bot

1. **Initialization:** The app automatically checks for and downloads required NLTK resources (`punkt`, `stopwords`, `wordnet`) if they are missing. It then computes the TF-IDF vectors for all 17 predefined FAQ questions.
2. **Preprocessing:** When a user asks a question, the input is converted to lowercase, punctuation is removed, it is tokenized into words, common English stopwords (like 'is', 'the', 'a') are removed, and words are lemmatized (reduced to their root form).
3. **Vectorization:** The cleaned user question is converted into a TF-IDF vector based on the vocabulary learned from the predefined FAQs.
4. **Matching:** Cosine similarity is used to calculate the angle (similarity) between the user's vector and each FAQ vector.
5. **Threshold:** The highest score is selected. If the score is below the `0.25` threshold, the bot returns a fallback response because the question is considered unrelated. Otherwise, it returns the mapped answer.

## Requirements

* Python 3.x
* Required packages listed in `requirements.txt`.
* Internet connection on the first run (to download NLTK data if it isn't locally cached).

## Installation

1. Clone or download this project.
2. Open a terminal and navigate to the project directory:
   ```bash
   cd CodeAlpha_FAQChatbot
   ```
3. Create a virtual environment:
   * **Windows**: `python -m venv .venv`
   * **macOS/Linux**: `python3 -m venv .venv`
4. Activate the virtual environment:
   * **Windows**: `.\.venv\Scripts\activate`
   * **macOS/Linux**: `source .venv/bin/activate`
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

Start the application:

```bash
python app.py
```

The application will run locally at `http://127.0.0.1:5000`.

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. Type a question in the chat input field (e.g., "Tell me about Python", "What is an internship?", "How do I submit my tasks?").
3. Press Enter or click the Send button.
4. The bot will respond with the most relevant FAQ answer, or a fallback message if it doesn't understand.

### Examples

**Direct Matches:**
* You: "What is Python?"
* Bot: "Python is a high-level, interpreted programming language..."

**Different Phrasing:**
* You: "Can you explain Python to me?"
* Bot: "Python is a high-level, interpreted programming language..."

**Unrelated Question:**
* You: "What is the weather today?"
* Bot: "Sorry, I couldn't find a relevant answer in the FAQ."

## CodeAlpha requirement mapping

* **FAQ collection** → Implemented (17 predefined Q&A pairs in `faq_data.py`).
* **NLP preprocessing** → Implemented using NLTK (lowercase, tokenization, lemmatization, stopword removal).
* **Similarity matching** → Implemented using `TfidfVectorizer` and `cosine_similarity` from scikit-learn.
* **Best matching FAQ answer** → Implemented (with a 0.25 threshold check).
* **Simple chat UI** → Implemented (Vanilla HTML/CSS/JS without unnecessary frontend frameworks).
