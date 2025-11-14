#file: services/clients/base_client.py
# Alap kliensosztály – egységes interfészt biztosít a különböző AI kliensekhez.


class BaseClient:
    """Alap AI kliens interfész, amely a minimális chat funkciót írja elő."""

    def chat(self, prompt: str) -> str:
        """Szöveges válasz generálása. A gyermekosztály implementálja."""
        raise NotImplementedError("A chat metódust implementálni kell a gyermek osztályban.")
