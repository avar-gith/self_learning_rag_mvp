#file: services/chunking/chunk_service.py
# Chunkolás – tudáselemek feldarabolása ~400 karakter körül, mondathatáron, átfedés nélkül.

from typing import List


class KnowledgeChunkerService:
    """
    KnowledgeChunkerService
    -----------------------
    Egy egyszerű chunkoló szolgáltatás, amely egy hosszabb szöveget
    kb. 400 karakteres darabokra bont, lehetőség szerint mondathatáron.
    Átfedés nincs.
    """

    def __init__(self, max_chars: int = 400):
        """
        Inicializáló metódus.

        Paraméterek:
            max_chars (int): chunkonkénti karakterlimit (alapértelmezés: 400)
        """
        self.max_chars = max_chars

    def chunk_text(self, text: str) -> List[str]:
        """
        A megadott szöveget kb. 400 karakteres chunkokra darabolja.
        Elsőként megpróbál mondathatáron vágni (. ? ! után), ha lehet.

        Visszatérési érték:
            List[str]: chunkolt szövegek listája
        """

        if not text or not text.strip():
            return []

        text = text.strip()
        chunks = []

        start = 0
        length = len(text)

        while start < length:
            # Ha a maradék kisebb, mint a limit → maradék egészben chunk
            if length - start <= self.max_chars:
                chunks.append(text[start:].strip())
                break

            # Nézzük meg a vágási pontot kb. 400 karakternél
            end = start + self.max_chars
            candidate = text[start:end]

            # Keressük meg az utolsó mondatzáró jelet (., ?, !)
            split_pos = max(
                candidate.rfind(". "),
                candidate.rfind("? "),
                candidate.rfind("! ")
            )

            if split_pos == -1:
                # Nincs mondathatár → vágunk 400 karakter után
                split_pos = self.max_chars
            else:
                # A mondatzáró jel után vágunk
                split_pos += 2  # ". " vagy "? " vagy "! "

            chunk = text[start:start + split_pos].strip()
            chunks.append(chunk)

            start += split_pos

        return chunks


# -------------------------------------------------------------------------
# Helper függvény a könnyebb híváshoz
# -------------------------------------------------------------------------
def chunk_text(text: str, max_chars: int = 400) -> List[str]:
    service = KnowledgeChunkerService(max_chars=max_chars)
    return service.chunk_text(text)
