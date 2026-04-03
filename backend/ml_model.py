from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class SpamDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        self.model = MultinomialNB()
        self.is_fitted = False
        self._train_dummy_model()

    def _train_dummy_model(self):
        # A tiny dataset to allow the model to predict something meaningful
        texts = [
            "Win a free iPhone click here",
            "Urgent account update required immediately",
            "Congratulations you have won $1000",
            "Get rich quick with this one weird trick",
            "Buy cheap pills online now",
            "Earn money from home effortlessly",
            "Hello, how are you doing today?",
            "Can we reschedule our meeting to 5 PM?",
            "Don't forget to pick up the groceries.",
            "I'll send you the report by tomorrow morning.",
            "Sounds good, see you then!",
            "Thanks for the update, let's discuss this later."
        ]
        labels = [
            "Spam", "Spam", "Spam", "Spam", "Spam", "Spam",
            "Safe", "Safe", "Safe", "Safe", "Safe", "Safe"
        ]
        
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_fitted = True

    def predict(self, text: str):
        if not text.strip():
            return "Safe", 1.0

        X = self.vectorizer.transform([text])
        prediction = self.model.predict(X)[0]
        
        # Calculate a mock confidence score from probabilities
        probabilities = self.model.predict_proba(X)[0]
        confidence = float(max(probabilities))
        
        # Just to make it slightly more dynamic for unseen words
        if prediction == "Safe" and any(word in text.lower() for word in ['win', 'free', 'click', 'urgent', 'money', 'prize', 'viagra', 'bank', 'password']):
             prediction = "Spam"
             confidence = 0.85
             
        return prediction, round(confidence, 2)

spam_detector = SpamDetector()
