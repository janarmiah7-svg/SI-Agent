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
        tokens = {normalize(record["name"]), *(normalize(alias) for alias in aliases)}
        matches = [entity for entity in entities if entity["_tokens"] & tokens]

        if not matches:
            entities.append(
                {
                    "canonical_name": record["name"],
                    "aliases": aliases,
                    "sources": {record["source"]},
                    "_tokens": set(tokens),
                }
            )
            continue

        primary = matches[0]
        primary["sources"].add(record["source"])
        primary["aliases"].update(aliases)
        primary["_tokens"].update(tokens)

        if normalize(record["name"]) != normalize(primary["canonical_name"]):
            primary["aliases"].add(record["name"])

        for extra in matches[1:]:
            primary["sources"].update(extra["sources"])
            primary["aliases"].update(extra["aliases"])
            primary["_tokens"].update(extra["_tokens"])
            entities.remove(extra)

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


def find_entity(query: str, records: list[dict] | None = None) -> dict | None:
    """Return the merged entity that matches *query*."""
    needle = normalize(query)
    entities = MERGED_SOURCE_RECORDS if records is None else merge_records(records)
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

    aliases = ", ".join(entity["aliases"]) or "brak aliasów"
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
