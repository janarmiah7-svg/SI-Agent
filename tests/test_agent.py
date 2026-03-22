"""
Tests for the SI-Agent concert ticket functionality.
"""

import pytest

from agent import NOT_UNDERSTOOD, process_query
from tickets import (
    HANS_ZIMMER_CONCERTS,
    extract_city,
    format_ticket,
    get_hans_zimmer_tickets,
    is_availability_query,
    is_hans_zimmer_query,
    is_ticket_query,
)


# ---------------------------------------------------------------------------
# is_availability_query
# ---------------------------------------------------------------------------

class TestIsAvailabilityQuery:
    def test_masz_te_bilety(self):
        assert is_availability_query("masz te bilety?") is True

    def test_masz_bilety(self):
        assert is_availability_query("masz bilety") is True

    def test_czy_masz_bilety(self):
        assert is_availability_query("czy masz bilety na to?") is True

    def test_macie_bilety(self):
        assert is_availability_query("macie bilety na Hans Zimmer?") is True

    def test_masz_te_pasy(self):
        assert is_availability_query("masz te pasy?") is True

    def test_case_insensitive(self):
        assert is_availability_query("Masz Te Bilety?") is True

    def test_english(self):
        assert is_availability_query("do you have tickets") is True

    def test_unrelated(self):
        assert is_availability_query("jaka jest pogoda") is False

    def test_hans_zimmer_named_query_not_availability(self):
        assert is_availability_query("bilety na koncert hansa zimmera") is False


# ---------------------------------------------------------------------------
# is_hans_zimmer_query
# ---------------------------------------------------------------------------

class TestIsHansZimmerQuery:
    def test_full_name(self):
        assert is_hans_zimmer_query("Hans Zimmer") is True

    def test_polish_genitive(self):
        assert is_hans_zimmer_query("bilety hansa zimmera") is True

    def test_typo_in_concert_keyword(self):
        # The original query contains "hansa zimmera"
        assert is_hans_zimmer_query("pasy na konceryt hansa zimmera") is True

    def test_case_insensitive(self):
        assert is_hans_zimmer_query("HANS ZIMMER") is True

    def test_unrelated(self):
        assert is_hans_zimmer_query("bilety na koncert Coldplay") is False


# ---------------------------------------------------------------------------
# is_ticket_query
# ---------------------------------------------------------------------------

class TestIsTicketQuery:
    def test_bilety(self):
        assert is_ticket_query("bilety na koncert") is True

    def test_pasy(self):
        assert is_ticket_query("pasy na konceryt hansa zimmera") is True

    def test_concert_keyword(self):
        assert is_ticket_query("Hans Zimmer concert") is True

    def test_unrelated(self):
        assert is_ticket_query("gdzie jest sklep") is False


# ---------------------------------------------------------------------------
# get_hans_zimmer_tickets
# ---------------------------------------------------------------------------

class TestGetHansZimmerTickets:
    def test_returns_all_by_default(self):
        tickets = get_hans_zimmer_tickets()
        assert len(tickets) == len(HANS_ZIMMER_CONCERTS)

    def test_filter_by_city(self):
        tickets = get_hans_zimmer_tickets("Warszawa")
        assert all(t.city.lower() == "warszawa" for t in tickets)
        assert len(tickets) >= 1

    def test_filter_by_city_case_insensitive(self):
        tickets = get_hans_zimmer_tickets("warszawa")
        assert len(tickets) >= 1

    def test_filter_nonexistent_city(self):
        tickets = get_hans_zimmer_tickets("Nieistniejące")
        assert tickets == []


# ---------------------------------------------------------------------------
# extract_city
# ---------------------------------------------------------------------------

class TestExtractCity:
    def test_warszawa(self):
        assert extract_city("bilety Warszawa Hans Zimmer") == "Warszawa"

    def test_krakow_no_diacritic(self):
        result = extract_city("Hans Zimmer krakow")
        assert result is not None
        assert "krak" in result.lower()

    def test_no_city(self):
        assert extract_city("pasy na konceryt hansa zimmera") is None


# ---------------------------------------------------------------------------
# format_ticket
# ---------------------------------------------------------------------------

class TestFormatTicket:
    def test_contains_event_name(self):
        ticket = HANS_ZIMMER_CONCERTS[0]
        text = format_ticket(ticket)
        assert ticket.event in text

    def test_contains_venue(self):
        ticket = HANS_ZIMMER_CONCERTS[0]
        text = format_ticket(ticket)
        assert ticket.venue in text

    def test_contains_url(self):
        ticket = HANS_ZIMMER_CONCERTS[0]
        text = format_ticket(ticket)
        assert ticket.url in text

    def test_extra_shown_when_present(self):
        sold_out = next(t for t in HANS_ZIMMER_CONCERTS if t.extra)
        text = format_ticket(sold_out)
        assert sold_out.extra in text


# ---------------------------------------------------------------------------
# process_query (agent integration)
# ---------------------------------------------------------------------------

class TestProcessQuery:
    def test_original_polish_query(self):
        response = process_query("podaj mi pasy na konceryt hansa zimmera")
        assert "Hans Zimmer" in response
        assert "ticketmaster" in response.lower() or "bilet" in response.lower()

    def test_english_query(self):
        response = process_query("tickets for Hans Zimmer concert")
        assert "Hans Zimmer" in response

    def test_city_filter_applied(self):
        response = process_query("bilety Hansa Zimmera Kraków")
        assert "Kraków" in response or "krak" in response.lower()

    def test_empty_query_returns_greeting(self):
        response = process_query("")
        assert "SI-Agent" in response or "bilety" in response.lower()

    def test_unrelated_query_not_understood(self):
        response = process_query("jaka jest pogoda w Warszawie")
        assert response == NOT_UNDERSTOOD

    def test_masz_te_bilety_returns_tickets(self):
        response = process_query("masz te bilety?")
        assert "Tak, mam bilety" in response
        assert "Hans Zimmer" in response
        assert "ticketmaster" in response.lower()

    def test_masz_bilety_returns_all_concerts(self):
        response = process_query("masz bilety")
        assert "Hans Zimmer" in response
        for ticket in HANS_ZIMMER_CONCERTS:
            assert ticket.venue in response

    def test_czy_masz_bilety_returns_tickets(self):
        response = process_query("czy masz bilety na to?")
        assert "Tak, mam bilety" in response
