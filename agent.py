"""
SI-Agent — Sztuczna Inteligencja Agent
An agent that handles natural language queries (Polish/English) about concert tickets.

Usage:
    python agent.py
    python agent.py "podaj mi pasy na konceryt hansa zimmera"
"""

import sys

from tickets import (
    extract_city,
    format_ticket,
    get_hans_zimmer_tickets,
    is_availability_query,
    is_hans_zimmer_query,
    is_ticket_query,
)

GREETING = "Witaj! Jestem SI-Agent. Mogę pomóc Ci znaleźć bilety na koncerty."
HELP_TEXT = (
    "Spróbuj zapytać o bilety np.:\n"
    "  - podaj mi bilety na koncert Hansa Zimmera\n"
    "  - pasy na konceryt hansa zimmera\n"
    "  - Hans Zimmer Kraków\n"
    "  - wyjdź / exit — aby zakończyć"
)
NOT_UNDERSTOOD = (
    "Nie rozumiem tego zapytania. "
    "Spróbuj zapytać o bilety na koncert, np. 'bilety na koncert Hansa Zimmera'."
)


def process_query(query: str) -> str:
    """
    Process a natural language query and return an appropriate response.

    Args:
        query: User query string (Polish or English).

    Returns:
        Agent response as a string.
    """
    if not query or not query.strip():
        return GREETING + "\n\n" + HELP_TEXT

    text = query.strip()

    if is_availability_query(text):
        tickets = get_hans_zimmer_tickets()
        header = "Tak, mam bilety! Oto dostępne bilety na koncert Hansa Zimmera:\n"
        sections = [header]
        for i, ticket in enumerate(tickets, 1):
            sections.append(f"[{i}]\n{format_ticket(ticket)}")
        sections.append(
            "\nKup bilety bezpośrednio przez podane linki lub odwiedź ticketmaster.pl"
        )
        return "\n\n".join(sections)

    if is_hans_zimmer_query(text) and is_ticket_query(text):
        city = extract_city(text)
        tickets = get_hans_zimmer_tickets(city)

        if not tickets:
            return (
                f"Nie znaleziono biletów na koncert Hansa Zimmera"
                + (f" w mieście '{city}'" if city else "")
                + ".\nSpróbuj inne miasto lub sprawdź dostępność na ticketmaster.pl"
            )

        header = "Oto dostępne bilety na koncert Hansa Zimmera"
        if city:
            header += f" w mieście {city.capitalize()}"
        header += ":\n"

        sections = [header]
        for i, ticket in enumerate(tickets, 1):
            sections.append(f"[{i}]\n{format_ticket(ticket)}")

        sections.append(
            "\nKup bilety bezpośrednio przez podane linki lub odwiedź ticketmaster.pl"
        )
        return "\n\n".join(sections)

    return NOT_UNDERSTOOD


def run_interactive() -> None:
    """Run the agent in interactive (REPL) mode."""
    print(GREETING)
    print(HELP_TEXT)
    print()

    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDo widzenia!")
            break

        if user_input.lower() in ("wyjdź", "wyjdz", "exit", "quit", "q"):
            print("Do widzenia!")
            break

        if not user_input:
            continue

        response = process_query(user_input)
        print(f"\nAgent: {response}\n")


def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(process_query(query))
    else:
        run_interactive()


if __name__ == "__main__":
    main()
