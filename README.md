# SI-Agent

SI-Agent (Sztuczna Inteligencja Agent) jest agentem obsługującym zapytania w języku polskim i angielskim dotyczące biletów na koncerty.

## Użycie

```bash
# Zapytanie jednorazowe
python agent.py "podaj mi pasy na konceryt hansa zimmera"

# Tryb interaktywny (REPL)
python agent.py
```

## Przykładowe zapytania

- `podaj mi bilety na koncert Hansa Zimmera`
- `pasy na konceryt hansa zimmera`
- `bilety Hansa Zimmera Kraków`
- `Hans Zimmer tickets Warsaw`

## Testy

```bash
python -m pytest tests/ -v
```

## Struktura projektu

```
agent.py      — główna logika agenta
tickets.py    — dane i funkcje dot. biletów na koncerty
tests/        — testy jednostkowe
```
