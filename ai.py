
import json
from ollama import chat


def get_book_recommendations(preferences):
    try:
        response = chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are BookMatch. Recommend exactly five real books "
                        "based on the reader's preferences. "
                        "Respect their genre, reading level, mood, length, "
                        "and anything they want to avoid. "
                        "Return only valid JSON. Keep explanations short."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Preferences: {json.dumps(preferences)}\n"
                        "Return a JSON object with a books array. "
                        "Each book needs title, author, why, "
                        "genre_score, story_score, and difficulty_score. "
                        "Scores must be integers from 0 to 10. "
                        "Recommend exactly five books."
                    )
                }
            ],
            format="json",
            options={
                "temperature": 0.2,
                "num_predict": 650
            }
        )

        data = json.loads(response.message.content)
        books = data.get("books", [])

        results = []

        for book in books[:5]:
            genre = max(0, min(10, int(book["genre_score"])))
            story = max(0, min(10, int(book["story_score"])))
            difficulty = max(0, min(10, int(book["difficulty_score"])))

            score = round(
                (genre * 0.4 + story * 0.4 + difficulty * 0.2) * 10
            )

            results.append(
                f"{book['title']} - {book['author']}\n"
                f"Match: {score}%\n"
                f"Why: {book['why']}"
            )

        return "\n\n".join(results) if results else None

    except Exception as e:
        print(f"Recommendation error: {e}")
        return None
