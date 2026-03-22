# SI-Agent

A simple Python search agent (wyszukiwarka postaci) for looking up characters by name or alias.

## Usage

```bash
python agent.py
```

Example search queries:
- `Gandalf` — returns Gandalf (stary złodziej)
- `stary złodziej` — returns Gandalf by alias

## Running tests

```bash
python -m pytest test_agent.py -v
```