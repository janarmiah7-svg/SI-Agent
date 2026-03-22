"""SI-Agent – prosty agent odpowiadający na pytania.

SI-Agent – a simple question-answering agent.
"""

KNOWLEDGE_BASE = {
    "czemu gandalf ma brode": (
        "Gandalf ma brodę, ponieważ przybrał postać starego, mądrego czarnoksiężnika. "
        "Jako Maiar – duchowa istota posłana do Śródziemia – Gandalf sam wybrał sobie "
        "ludzkie ciało (fana) o wyglądzie sędziwego starca z białą brodą, laską i kapeluszem. "
        "Taki wygląd miał wzbudzać zaufanie i szacunek wśród mieszkańców Śródziemia, "
        "a zarazem przypominać im o mądrości i doświadczeniu. "
        "Broda jest więc celowym elementem jego fizycznej manifestacji jako Istari (czarodzieja)."
    ),
    "why does gandalf have a beard": (
        "Gandalf has a beard because he chose the appearance of a wise old wizard. "
        "As a Maia – a spiritual being sent to Middle-earth – Gandalf deliberately took on "
        "a physical form (fana) resembling a venerable old man with a white beard, staff, and hat. "
        "This appearance was intended to inspire trust and respect among the peoples of Middle-earth "
        "and to signal his wisdom and age. "
        "The beard is therefore an intentional part of his physical manifestation as one of the Istari (wizards)."
    ),
}


def normalize(text: str) -> str:
    """Return a lower-cased, stripped version of *text*."""
    return text.strip().lower()


def ask(question: str) -> str:
    """Return an answer to *question*, or a default message if unknown."""
    key = normalize(question)
    if key in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[key]
    return (
        "Przepraszam, nie znam odpowiedzi na to pytanie. / "
        "Sorry, I don't know the answer to that question."
    )


def main() -> None:
    print("SI-Agent – wpisz pytanie lub 'koniec'/'exit' aby zakończyć.")
    print("SI-Agent – type your question or 'koniec'/'exit' to quit.\n")
    while True:
        try:
            question = input("Pytanie / Question: ")
        except (EOFError, KeyboardInterrupt):
            print("\nDo widzenia! / Goodbye!")
            break
        if normalize(question) in ("koniec", "exit", "quit"):
            print("Do widzenia! / Goodbye!")
            break
        print(f"\nOdpowiedź / Answer:\n{ask(question)}\n")


if __name__ == "__main__":
    main()
