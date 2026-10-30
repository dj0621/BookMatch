
import requests
from difflib import SequenceMatcher
from functools import lru_cache


def similarity(first, second):
    return SequenceMatcher(
        None,
        first.lower().strip(),
        second.lower().strip()
    ).ratio()


@lru_cache(maxsize=200)
def search_book(title, author):
    url = "https://openlibrary.org/search.json"

    params = {
        "title": title,
        "author": author,
        "fields": "key,title,author_name,cover_i",
        "limit": 5
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers={"User-Agent": "BookMatch/1.0"},
            timeout=10
        )

        response.raise_for_status()
        results = response.json().get("docs", [])

        for book in results:
            book_title = book.get("title", "")
            authors = book.get("author_name", [])

            if not authors:
                continue

            if similarity(title, book_title) < 0.8:
                continue

            if not any(
                similarity(author, name) >= 0.7
                for name in authors
            ):
                continue

            cover_id = book.get("cover_i")
            book_key = book.get("key", "")

            return {
                "title": book_title,
                "author": authors[0],
                "image": (
                    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    if cover_id else None
                ),
                "link": (
                    f"https://openlibrary.org{book_key}"
                    if book_key.startswith("/works/") else None
                )
            }

    except requests.RequestException as e:
        print(f"Open Library error: {e}")

    return None
