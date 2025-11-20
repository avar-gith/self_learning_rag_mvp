#file: services/anonymization/anonymizer_service.py
# Egyszerű, mintaalapú szöveg-anonimizáló service.
# Magyar nyelvre optimalizált PII mintákat tartalmaz, de MVP szinten tartjuk.

import re


# ────────────────────────────────────────────────────────────────
# 🇭🇺 Alap magyar PII minták (egyszerűsített verzió)
# ────────────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?36|06)?[\s-]?(?:1|20|30|31|50|70|90)?[\s-]?\d{2,3}[\s-]?\d{3,4}(?!\d)")
IBAN_RE = re.compile(r"\bHU\d{2}(?:[\s-]?\d){26}\b", re.IGNORECASE)
CARD_RE = re.compile(r"(?<!\d)(?:\d{4}[-\s]?){3}\d{4}(?!\d)")

# Hosszú számok – azonosítók, ügyfélszámok stb.
LONG_NUMBER_RE = re.compile(r"(?<!\d)\d{6,}(?!\d)")

# Egyszerűsített magyar cím minta
ADDRESS_RE = re.compile(
    r"\b([A-ZÁÉÍÓÖŐÚÜŰ][\wÁÉÍÓÖŐÚÜŰ\- ]+?)\s+"
    r"(utca|u\.|út|tér|krt\.|körút|köz|sétány|sugárút)\s+\d+[A-Za-z]?\b",
    re.IGNORECASE,
)

# Kimondott számok (MVP, 1–9)
DIGIT_WORD_RE = re.compile(
    r"\b(nulla|egy|kettő|ketto|két|harom|három|négy|negy|öt|ot|hat|hét|het|nyolc|kilenc)\b",
    re.IGNORECASE
)

# Felesleges whitespace-ek
MULTISPACE_RE = re.compile(r"\s{2,}")


# ────────────────────────────────────────────────────────────────
# 🇭🇺 Alap anonimizáló osztály
# ────────────────────────────────────────────────────────────────
class TextAnonymizerService:
    """
    Magyar nyelvű PII anonimizáló szolgáltatás.
    Egyelőre mintaalapú, nem használ NER-t, de később bővíthető.
    """

    def __init__(self):
        self.enabled = True

    def anonymize_text(self, input_text: str) -> str:
        """
        A bemeneti szöveg mintaalapú tisztítása.
        """
        if not input_text or not input_text.strip():
            return input_text

        if not self.enabled:
            return input_text

        s = input_text

        # 1) Email
        s = EMAIL_RE.sub("[EMAIL]", s)

        # 2) Telefonszám
        s = PHONE_RE.sub("[PHONE]", s)

        # 3) IBAN
        s = IBAN_RE.sub("[IBAN]", s)

        # 4) Bankkártyaszám
        s = CARD_RE.sub("[CARD]", s)

        # 5) Cím
        s = ADDRESS_RE.sub("[ADDRESS]", s)

        # 6) Egyszerű kimondott számok
        s = DIGIT_WORD_RE.sub("[SZÁM]", s)

        # 7) Hosszú numerikus azonosítók
        s = LONG_NUMBER_RE.sub("[ID]", s)

        # 8) Whitespace normalizálás
        s = MULTISPACE_RE.sub(" ", s).strip()

        return s


# ────────────────────────────────────────────────────────────────
# Helper – ha nem akarunk osztályt példányosítani
# ────────────────────────────────────────────────────────────────
def anonymize_text(input_text: str) -> str:
    service = TextAnonymizerService()
    return service.anonymize_text(input_text)
