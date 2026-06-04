from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def detect_intent(query, intents):

    phrases = []
    labels = []

    for intent, examples in intents.items():
        for example in examples:
            phrases.append(example)
            labels.append(intent)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        phrases + [query]
    )

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_match = similarity.argmax()
    confidence = similarity.max()

    if confidence > 0.30:
        return labels[best_match]

    return None