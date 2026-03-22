"""SI-Agent – prosty agent odpowiadający na pytania."""

from __future__ import annotations

import re
import unicodedata

DEFAULT_ANSWER = (
    "Przepraszam, nie znam odpowiedzi na to pytanie. / "
    "Sorry, I don't know the answer to that question."
)

USA_COLLAPSE_ANSWER = (
    "Nie ma daty upadku USA, ponieważ Stany Zjednoczone nie upadły. "
    "Jeśli chcesz, mogę podać informacje o kryzysach politycznych, gospodarczych "
    "albo o konkretnym okresie w historii USA."
)


def normalize(text: str) -> str:
    """Return a stripped, lower-cased, ASCII-normalized version of *text*."""
    normalized = unicodedata.normalize("NFKD", text.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", ascii_text)


def is_usa_collapse_date_question(question: str) -> bool:
    """Return True when *question* asks for a supposed date of USA's collapse."""
    normalized = normalize(question)
    required_terms = ("podaj", "date", "upadku", "usa")
    return all(term in normalized for term in required_terms)


def ask(question: str) -> str:
    """Return an answer to *question*, or a default message if unknown."""
    if is_usa_collapse_date_question(question):
        return USA_COLLAPSE_ANSWER
    return DEFAULT_ANSWER


def main() -> None:
    """Run the interactive CLI."""
    print("SI-Agent – wpisz pytanie lub 'koniec'/'exit' aby zakończyć.")
    while True:
        try:
            question = input("Pytanie: ")
        except (EOFError, KeyboardInterrupt):
            print("\nDo widzenia!")
            break
        if normalize(question) in {"koniec", "exit", "quit"}:
            print("Do widzenia!")
            break
        print(ask(question))


if __name__ == "__main__":
    main()
