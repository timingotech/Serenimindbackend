import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Load and preprocess the dataset
df = pd.read_csv('C:/Users/user/Desktop/ML/CommunitySentiment/train.csv', encoding='ISO-8859-1')
df = df.dropna(subset=['sentiment'])
X = df['text'].fillna('')
y = df['sentiment']

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
svm = SVC(kernel='linear', random_state=42)
svm.fit(X_vec, y)

def predict_sentiment(text):
    text_vec = vectorizer.transform([text])
    prediction = svm.predict(text_vec)
    return prediction[0]
