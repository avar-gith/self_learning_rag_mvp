#file: services/rag/prompt_builder.py
# Prompt Builder modul – a RAG pipeline által talált chunkokból
# teljes, LLM-barát promptot építünk fel.

"""
A modul feladata:
- Összegyűjteni a releváns chunkokat
- Kontekstus-blokkot létrehozni
- A felhasználói kérdést és a feladat-szöveget hozzáadni
- Egyetlen, jól strukturált prompt stringet visszaadni
"""


def build_prompt(query: str, rag_results):
    """
    Prompt összeállítása a RAG eredményekből.

    Paraméterek:
        query (str): felhasználó kérdése
        rag_results (List[(KnowledgeChunk, similarity)]):
            a RAGService által talált chunk + similarity párok

    Visszatér:
        str: a LLM-nek átadható prompt
    """

    # Chunkok összegyűjtése
    if rag_results:
        context_text = "\n\n".join(
            f"- {chunk.content}"
            for chunk, _sim in rag_results
        )
    else:
        context_text = "(Nem találtunk releváns tartalmat a tudásbázisban.)"

    # Végső prompt
    prompt = f"""
Te egy középiskolásokat támogató általános AI vagy. 
A feladatod, hogy a megadott kontextus alapján bővebben, oktató stílustban válaszolj érthetően, pontosan, magyar nyelven.
Ha a kontextus nem tartalmaz elegendő választ, azt is egyértelműen jelezd.

### KONTEKSTUS:
{context_text}

### FELHASZNÁLÓI KÉRDÉS:
{query}

### FELADAT:
A kontextus alapján adj világos, tömör, de pontos választ.
Ha hiányos a kontextus, jelezd külön.
"""

    # Whitespace normalizálás (esztétikai)
    return "\n".join(line.rstrip() for line in prompt.split("\n")).strip()
