
WEIGHTS = {
    "genre": 25,
    "description": 20,
    "favorite_book": 10,
    "book_mood": 10,
    "reading_level": 10,
    "book_length": 10,
    "setting": 5,
    "pace": 5,
    "series": 5
}


def calculate_match(ratings):
    total = 0
    maximum = 0

    for category, weight in WEIGHTS.items():
        rating = ratings.get(category)

        if rating is None:
            continue

        rating = max(0, min(10, float(rating)))

        total += (rating / 10) * weight
        maximum += weight

    if maximum == 0:
        return 0

    return round((total / maximum) * 100)
