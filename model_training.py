import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import SVC
import joblib

# Download stopwords
nltk.download('stopwords')

# Load the dataset
df = pd.read_csv('insurance_intents.csv')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation
    tokens = text.split()  # Tokenize text
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    return ' '.join(tokens)

# Apply preprocessing
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Convert text to feature vectors using TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)  # Use TF-IDF for better feature representation
X = vectorizer.fit_transform(df['cleaned_text'])
y = df['intent']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use a more powerful model like Support Vector Classifier
model = SVC(kernel='linear')

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model for later use
joblib.dump(model, 'insurance_intent_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
