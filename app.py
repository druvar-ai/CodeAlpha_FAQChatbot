import os
import string
import nltk
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faq_data import faq_data

# --- NLTK Setup ---
def setup_nltk():
    """Ensure required NLTK data is downloaded."""
    required_packages = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            try:
                nltk.data.find(f'corpora/{package}')
            except LookupError:
                 nltk.download(package, quiet=True)

setup_nltk()

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# --- NLP Preprocessing ---
def preprocess_text(text):
    """
    1. Lowercase
    2. Remove punctuation
    3. Tokenize
    4. Remove stopwords
    5. Lemmatize
    """
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    
    cleaned_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words
    ]
    
    return " ".join(cleaned_tokens)

# --- Pre-compute FAQ Vectors ---
# We keep questions separate to vectorize them
faq_questions = [item['question'] for item in faq_data]
preprocessed_faqs = [preprocess_text(q) for q in faq_questions]

# Initialize and fit TF-IDF vectorizer on the FAQs
vectorizer = TfidfVectorizer()
faq_tfidf_matrix = vectorizer.fit_transform(preprocessed_faqs)

# --- Flask App ---
app = Flask(__name__)

# Minimum similarity threshold
SIMILARITY_THRESHOLD = 0.25

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    # 1. Validate request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON."}), 400
        
    data = request.get_json()
    question = data.get("question", "")
    
    # 2. Validate question
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "Please enter a question."}), 400
        
    if len(question) > 500:
        return jsonify({"error": "Question is too long. Please keep it under 500 characters."}), 400

    try:
        # 3. Preprocess user question
        cleaned_question = preprocess_text(question)
        
        # If preprocessing removes all words (e.g. only stopwords were entered)
        if not cleaned_question:
             return jsonify({
                 "answer": "Sorry, I couldn't find a relevant answer in the FAQ. Your question might be too vague.",
                 "matched_question": None
             }), 200

        # 4. Calculate TF-IDF for the user question
        user_tfidf = vectorizer.transform([cleaned_question])
        
        # 5. Calculate cosine similarity against all FAQs
        similarities = cosine_similarity(user_tfidf, faq_tfidf_matrix).flatten()
        
        # 6. Find the highest-scoring FAQ
        best_match_idx = similarities.argmax()
        best_score = similarities[best_match_idx]
        
        # 7. Check threshold
        if best_score < SIMILARITY_THRESHOLD:
            return jsonify({
                "answer": "Sorry, I couldn't find a relevant answer in the FAQ.",
                "matched_question": None
            }), 200
            
        # 8. Return best match
        best_faq = faq_data[best_match_idx]
        return jsonify({
            "answer": best_faq["answer"],
            "matched_question": best_faq["question"]
        }), 200

    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
