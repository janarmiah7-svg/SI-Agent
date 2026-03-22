"""
SI-Agent - Simple search agent for characters.
"""

CHARACTERS = {
    "gandalf": {
        "name": "Gandalf",
        "alias": "stary złodziej",
        "description": (
            "Gandalf - stary złodziej i czarodziej, znany również jako Szary Pielgrzym. "
            "W 'Hobbicie' Tolkiena Gandalf werbuje Bilbo Bagginsa jako włamywacza "
            "dla kompanii Thorina Dębowej Tarczy."
        ),
        "origin": "J.R.R. Tolkien - Hobbit / Władca Pierścieni",
    },
    "bilbo": {
        "name": "Bilbo Baggins",
        "alias": "włamywacz",
        "description": (
            "Bilbo Baggins - hobbit z Shire, którego Gandalf polecił jako włamywacza "
            "kompanii krasnoludów."
        ),
        "origin": "J.R.R. Tolkien - Hobbit",
    },
}


def search(query: str) -> list[dict]:
    """Search for a character by name or alias."""
    query_lower = query.strip().lower()
    results = []
    for character in CHARACTERS.values():
        if (
            query_lower in character["name"].lower()
            or query_lower in character["alias"].lower()
        ):
            results.append(character)
    return results


def main() -> None:
    print("SI-Agent - Wyszukiwarka postaci")
    print("================================")
    query = input("Wyszukaj postać (np. 'Gandalf' lub 'stary złodziej'): ").strip()
    results = search(query)
    if results:
        for result in results:
            print(f"\nImię:    {result['name']}")
            print(f"Alias:   {result['alias']}")
            print(f"Opis:    {result['description']}")
            print(f"Źródło:  {result['origin']}")
    else:
        print("Nie znaleziono żadnych wyników.")


if __name__ == "__main__":
    main()
