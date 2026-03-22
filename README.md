# SI-Agent

Prosty agent odpowiadający na pytania w języku polskim i angielskim.  
A simple question-answering agent that supports Polish and English.

## Uruchomienie / Running

```bash
python agent.py
```

Wpisz pytanie i naciśnij Enter. Wpisz `koniec` lub `exit`, aby zakończyć.  
Type a question and press Enter. Type `koniec` or `exit` to quit.

### Przykład / Example

```
Pytanie / Question: czemu gandalf ma brode

Odpowiedź / Answer:
Gandalf ma brodę, ponieważ przybrał postać starego, mądrego czarnoksiężnika.
Jako Maiar – duchowa istota posłana do Śródziemia – Gandalf sam wybrał sobie
ludzkie ciało (fana) o wyglądzie sędziwego starca z białą brodą, laską i kapeluszem.
...
```

## Testy / Tests

```bash
pip install pytest
python -m pytest test_agent.py -v
```
