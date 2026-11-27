
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

texts = [
    "I love this product",
    "This is amazing",
    "Very happy with the service",
    "Excellent experience",
    "I am very satisfied",
    "This is wonderful",
    "I hate this product",
    "Very bad experience",
    "Terrible service",
    "I am disappointed",
    "This is horrible",
    "Worst experience ever",
    "The product is okay",
    "It is average",
    "Nothing special",
    "The service is normal"
]

labels = [
    "Positive", "Positive", "Positive", "Positive",
    "Positive", "Positive", "Negative", "Negative",
    "Negative", "Negative", "Negative", "Negative",
    "Neutral", "Neutral", "Neutral", "Neutral"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)


@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    review = ""

    if request.method == "POST":
        review = request.form.get("review", "").strip()

        if review:
            data = vectorizer.transform([review])
            sentiment = model.predict(data)[0]

    return render_template("index.html", sentiment=sentiment, review=review)


if __name__ == "__main__":
    app.run(debug=True)
