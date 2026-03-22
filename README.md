# SI-Agent

Wspominamy tu o dobrych czasach Marka.
We also remember Marek's good times.

## Entity merge demo

This branch now contains a minimal Python demo that merges equivalent records from
multiple source labels (`CEIDG`, `KRS`, and `network_localization`) when they refer
to the same entity. In the example dataset, `Gandalf`, `Gandalf Szary`, and
`stary złodziej` are resolved as the same entity.

## Run

```bash
python agent.py
```

## Tests

```bash
python -m unittest -q
```
