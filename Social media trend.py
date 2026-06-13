import pandas as pd
import numpy as np
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score

from wordcloud import WordCloud

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


data = {
    "text": [
        "AI is trending worldwide",
        "Big billion sale today",
        "New iPhone launched",
        "Cricket match highlights",
        "Breaking political news",
        "Stock market hits record high",
        "New movie release trending",
        "Technology is evolving fast",
        "Election results announced",
        "Sports championship updates",
        "I am eating lunch",
        "Watching TV at home",
        "Going to sleep",
        "Having dinner",
        "Listening to songs",
        "Walking in the park",
        "Reading a book",
        "Cleaning my room",
        "Cooking food",
        "Taking rest"
    ],
    "trend": [1,1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0,0]
}

df = pd.DataFrame(data)

def clean_text(text):
    text = re.sub(r"http\S+", "", str(text))
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)

df['clean_text'] = df['text'].apply(clean_text)

text_all = " ".join(df['clean_text'])

wordcloud = WordCloud(width=800, height=400).generate(text_all)

plt.figure()
plt.imshow(wordcloud)
plt.axis('off')
plt.title("Word Cloud - Frequent Words")
plt.show()

vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(df['clean_text']).toarray()
y = df['trend']


trend_counts = df['trend'].value_counts()

plt.figure()
trend_counts.plot(kind='bar')
plt.title("Trending vs Not Trending")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

lin_model = LinearRegression()
lin_model.fit(X_train, y_train)

lin_pred = lin_model.predict(X_test)
lin_pred = [1 if p > 0.5 else 0 for p in lin_pred]

lin_acc = accuracy_score(y_test, lin_pred)

log_model = LogisticRegression()
log_model.fit(X_train, y_train)

log_pred = log_model.predict(X_test)
log_acc = accuracy_score(y_test, log_pred)

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['clean_text'])

X_seq = tokenizer.texts_to_sequences(df['clean_text'])
X_pad = pad_sequences(X_seq, maxlen=20)

X_train_rnn, X_test_rnn, y_train_rnn, y_test_rnn = train_test_split(
    X_pad, y, test_size=0.2, random_state=42)

rnn_model = Sequential()
rnn_model.add(Embedding(5000, 64, input_length=20))
rnn_model.add(LSTM(64))
rnn_model.add(Dense(1, activation='sigmoid'))

rnn_model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

rnn_model.fit(X_train_rnn, y_train_rnn,
              epochs=5,
              batch_size=2,
              verbose=1)

_, rnn_acc = rnn_model.evaluate(X_test_rnn, y_test_rnn)


df_numeric = df[['trend']]
corr = df_numeric.corr()

plt.figure()
sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()

print("\nModel Accuracies:")
print("Linear Regression:", lin_acc)
print("Logistic Regression:", log_acc)
print("RNN:", rnn_acc)

models = ['Linear', 'Logistic', 'RNN']
accuracies = [lin_acc, log_acc, rnn_acc]

plt.figure()
plt.bar(models, accuracies)
plt.title("Model Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.show()
