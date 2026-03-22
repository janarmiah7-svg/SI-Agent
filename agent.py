"""SI-Agent demo for merging equivalent entity records from multiple sources."""

from __future__ import annotations

import unicodedata

SOURCE_RECORDS = [
    {
        "source": "CEIDG",
        "name": "Gandalf",
        "aliases": ["Mithrandir"],
    },
    {
        "source": "KRS",
        "name": "Gandalf Szary",
        "aliases": ["Gandalf"],
    },
    {
        "source": "network_localization",
        "name": "stary złodziej",
        "aliases": ["Gandalf"],
    },
]


def normalize(text: str) -> str:
    """Normalize text for matching names and aliases."""
    folded = unicodedata.normalize("NFKD", text.strip().lower())
    folded = folded.translate(str.maketrans({"ł": "l"}))
    return "".join(char for char in folded if not unicodedata.combining(char))


def merge_records(records: list[dict]) -> list[dict]:
    """Merge source records that refer to the same entity."""
    entities: list[dict] = []

    for record in records:
        aliases = set(record.get("aliases", []))
        tokens = {normalize(record["name"])} | {
            normalize(alias) for alias in aliases if alias
        }
        match_indexes = [
            index for index, entity in enumerate(entities) if entity["_tokens"] & tokens
        ]

        if not match_indexes:
            entities.append(
                {
                    "canonical_name": record["name"],
                    "aliases": aliases,
                    "sources": {record["source"]},
                    "_tokens": set(tokens),
                }
            )
            continue

        primary = entities[match_indexes[0]]
        primary["sources"].add(record["source"])
        primary["aliases"].update(aliases)
        primary["_tokens"].update(tokens)

        if normalize(record["name"]) != normalize(primary["canonical_name"]):
            primary["aliases"].add(record["name"])

        for index in reversed(match_indexes[1:]):
            extra = entities[index]
            primary["sources"].update(extra["sources"])
            primary["aliases"].update(extra["aliases"])
            primary["_tokens"].update(extra["_tokens"])
            del entities[index]

    merged = []
    for entity in entities:
        merged.append(
            {
                "canonical_name": entity["canonical_name"],
                "aliases": sorted(
                    alias
                    for alias in entity["aliases"]
                    if normalize(alias) != normalize(entity["canonical_name"])
                ),
                "sources": sorted(entity["sources"]),
            }
        )
    return merged


MERGED_SOURCE_RECORDS = merge_records(SOURCE_RECORDS)
_records_cache: dict[tuple, list[dict]] = {}


def _records_cache_key(records: list[dict]) -> tuple:
    """Return a hashable cache key for a list of source records."""
    return tuple(
        (
            record["source"],
            record["name"],
            tuple(record.get("aliases", [])),
        )
        for record in records
    )


def find_entity(query: str, records: list[dict] | None = None) -> dict | None:
    """Return the merged entity that matches *query*."""
    needle = normalize(query)
    if records is None:
        entities = MERGED_SOURCE_RECORDS
    else:
        cache_key = _records_cache_key(records)
        entities = _records_cache.setdefault(cache_key, merge_records(records))
    for entity in entities:
        names = [entity["canonical_name"], *entity["aliases"]]
        if any(normalize(name) == needle for name in names):
            return entity
    return None


def describe_entity(query: str, records: list[dict] | None = None) -> str:
    """Describe how a query maps to a merged entity."""
    entity = find_entity(query, records)
    if entity is None:
        return "Nie znaleziono powiązanego bytu."

    aliases = ", ".join(entity["aliases"]) if entity["aliases"] else "brak aliasów"
    sources = ", ".join(entity["sources"])
    return (
        f"{entity['canonical_name']} to ten sam byt co: {aliases}. "
        f"Połączone źródła: {sources}."
    )


def main() -> None:
    query = input("Podaj nazwę lub alias bytu: ").strip()
    print(describe_entity(query))


if __name__ == "__main__":
    main()
