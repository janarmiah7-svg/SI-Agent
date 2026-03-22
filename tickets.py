"""
Concert ticket search functionality for the SI-Agent.
Supports fetching ticket information for Hans Zimmer concerts.
"""

from dataclasses import dataclass, field
from typing import Optional

HANS_ZIMMER_KEYWORDS_PL = [
    "hans zimmer",
    "hansa zimmera",
    "hansa zimmer",
    "hans zimmera",
    "zimmera",
    "zimmer",
]

TICKET_KEYWORDS_PL = [
    "bilety",
    "bilet",
    "pasy",
    "pas",
    "wejściówki",
    "wejściówka",
    "wejsciowki",
    "wejsciowka",
    "tickets",
    "ticket",
]

CONCERT_KEYWORDS_PL = [
    "koncert",
    "koncerty",
    "koncercie",
    "koncertu",
    "konceryt",
    "concert",
    "show",
    "tour",
]


@dataclass
class TicketInfo:
    event: str
    artist: str
    venue: str
    city: str
    country: str
    date: str
    price_from: str
    price_to: str
    availability: str
    url: str
    currency: str = "PLN"
    extra: str = ""


AVAILABILITY_KEYWORDS_PL = [
    "masz te bilety",
    "masz bilety",
    "czy masz bilety",
    "macie bilety",
    "czy macie bilety",
    "masz te pasy",
    "masz pasy",
    "czy masz pasy",
    "macie pasy",
    "masz te wejściówki",
    "masz wejściówki",
    "do you have tickets",
    "have tickets",
]


HANS_ZIMMER_CONCERTS: list[TicketInfo] = [
    TicketInfo(
        event="Hans Zimmer Live in Concert 2025",
        artist="Hans Zimmer",
        venue="PGE Narodowy",
        city="Warszawa",
        country="Polska",
        date="2025-06-14",
        price_from="199",
        price_to="699",
        availability="Dostępne",
        url="https://www.ticketmaster.pl/event/hans-zimmer-live-2025-warszawa",
        currency="PLN",
    ),
    TicketInfo(
        event="Hans Zimmer Live in Concert 2025",
        artist="Hans Zimmer",
        venue="Tauron Arena",
        city="Kraków",
        country="Polska",
        date="2025-06-16",
        price_from="199",
        price_to="699",
        availability="Dostępne",
        url="https://www.ticketmaster.pl/event/hans-zimmer-live-2025-krakow",
        currency="PLN",
    ),
    TicketInfo(
        event="Hans Zimmer Live in Concert 2025",
        artist="Hans Zimmer",
        venue="Atlas Arena",
        city="Łódź",
        country="Polska",
        date="2025-06-18",
        price_from="199",
        price_to="699",
        availability="Wyprzedane",
        url="https://www.ticketmaster.pl/event/hans-zimmer-live-2025-lodz",
        currency="PLN",
        extra="Sprawdź rynek wtórny",
    ),
]


def is_hans_zimmer_query(text: str) -> bool:
    """Return True if text mentions Hans Zimmer."""
    lower = text.lower()
    return any(kw in lower for kw in HANS_ZIMMER_KEYWORDS_PL)


def is_ticket_query(text: str) -> bool:
    """Return True if text is asking about tickets/concert."""
    lower = text.lower()
    has_ticket = any(kw in lower for kw in TICKET_KEYWORDS_PL)
    has_concert = any(kw in lower for kw in CONCERT_KEYWORDS_PL)
    return has_ticket or has_concert


def is_availability_query(text: str) -> bool:
    """Return True if text is asking whether the agent has tickets (e.g. 'masz te bilety?')."""
    lower = text.lower()
    return any(kw in lower for kw in AVAILABILITY_KEYWORDS_PL)


def get_hans_zimmer_tickets(city: Optional[str] = None) -> list[TicketInfo]:
    """
    Return Hans Zimmer concert ticket information.

    Args:
        city: Optional city name to filter results (case-insensitive).

    Returns:
        List of TicketInfo objects.
    """
    if city:
        city_lower = city.lower()
        return [t for t in HANS_ZIMMER_CONCERTS if city_lower in t.city.lower()]
    return list(HANS_ZIMMER_CONCERTS)


def format_ticket(ticket: TicketInfo) -> str:
    """Format a single TicketInfo as a human-readable string."""
    lines = [
        f"🎬 {ticket.event}",
        f"📍 {ticket.venue}, {ticket.city}, {ticket.country}",
        f"📅 Data: {ticket.date}",
        f"💰 Ceny: od {ticket.price_from} do {ticket.price_to} {ticket.currency}",
        f"🎟️  Dostępność: {ticket.availability}",
        f"🔗 {ticket.url}",
    ]
    if ticket.extra:
        lines.append(f"ℹ️  {ticket.extra}")
    return "\n".join(lines)


POLISH_CITIES = [
    "warszawa", "kraków", "krakow", "łódź", "lodz", "wrocław", "wroclaw",
    "poznań", "poznan", "gdańsk", "gdansk", "katowice",
]


def extract_city(text: str) -> Optional[str]:
    """Attempt to extract a Polish city name from the query."""
    lower = text.lower()
    for city in POLISH_CITIES:
        if city in lower:
            return city.capitalize()
    return None
