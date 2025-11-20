# self_learning_rag_mvp
**Minimális demonstrációs RAG rendszer tanulási és kísérletezési célokra**  
*(Django • Embedding pipeline • Tudásbázis • Chunking • Anonimizálás • LLM integráció)*

Ez a projekt egy oktató és minta célú **Retrieval-Augmented Generation (RAG)** rendszer,
amely bemutatja, hogyan épül fel egy modern, tudásbázisra épülő AI-megoldás.

A cél:  
egyszerű, átlátható és bővíthető MVP, amely alkalmas a RAG működésének tanulására,
tesztelésére, finomhangolására és további fejlesztések alapjának.

---

## 🚀 Funkcionalitások

A demó bemutatja a RAG-pipeline fő elemeit:

### 🔹 Tudásbázis kezelés
- Kategóriák és tudáselemek (Knowledge Items)
- Dinamikus kategóriadetektálás LLM-mel  
- Automatikus slug-generálás  
- Admin felület a tartalom kezeléséhez (Django admin)

### 🔹 Chunking (darabolás)
A hosszabb tartalmak a rendszerben automatikusan több **chunkra** osztódnak,  
amelyek külön kerülnek beágyazásra, hogy finomabb keresés legyen lehetséges.

### 🔹 Embedding készítés
- Minden chunk embeddinget kap
- OpenAI / más modell könnyen cserélhető
- Embeddingek tárolása adatbázisban

### 🔹 Classic + Embedding keresés
A RAG tesztfelület kétféle keresést futtat:

- **klasszikus szövegkeresés**  
- **embedding-alapú hasonlóság keresés (cosine similarity)**

Mindkettő eredménye látható a UI-ban.

### 🔹 Anonimizálás (opcionális)
A rendszer képes automatikusan PII-mentesített  
„anonymized_content” mezőt előállítani, amelyet a RAG pipeline használhat.

### 🔹 LLM válasz generálás
A releváns chunkokból egy strukturált prompt épül,  
majd a kiválasztott LLM (OpenAI / Claude / stb.) elkészíti a végső választ.

---

## 🧠 RAG pipeline áttekintés

1. **Felhasználó kérdez**
2. **LLM kategóriadetektálás**  
   – a rendszer kiválasztja a releváns tudáskategóriát  
3. **Classic Search**  
   – cím, tartalom, chunk szöveg alapján
4. **Embedding Search**  
   – cosine similarity alapján
5. **Chunkok kiválasztása Top-K + threshold alapján**
6. **Prompt összeállítás**
7. **LLM válasz generálása kontextussal**

---

## 🖥️ Interaktív tesztfelületek

A projekt két fő UI-t tartalmaz:

### 🔸 `/ai/rag-test`
- Query input
- TOP-K és threshold beállítás
- LLM modellválasztó
- Kategóriadetektálás eredménye
- Klasszikus találatok listája
- Embedding találatok score-ral
- Végső LLM válasz

### 🔸 `/ai/test`
Egyszerű többmodelles LLM teszt chatfelület.

---

## 🛠️ Technológiai stack

- **Python 3.11+**
- **Django 5**
- **SQLite (alapértelmezett) vagy Postgres**
- **OpenAI / kompatibilis LLM provider**
- **Bootstrap alapú frontend komponensek**
- (Opcionálisan: ElasticSearch — integrálható későbbi verzióban)

---

## 📦 Telepítés és futtatás

### 1. Repo klónozása
git clone https://github.com/<user>/self_learning_rag_mvp.git
cd self_learning_rag_mvp
2. Virtuális környezet
bash
Kód másolása
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Függőségek telepítése
bash
Kód másolása
pip install -r requirements.txt
4. Migrációk futtatása
bash
Kód másolása
python manage.py migrate
5. Developer server indítása
bash
Kód másolása
python manage.py runserver

🧪 Tudáselemek betöltése (seed parancsok)

A projekt külön management parancsokat tartalmaz:

python manage.py seed_default_knowledge
python manage.py seed_poet_knowledge
python manage.py seed_geo_knowledge


Mindegyik külön témakörrel tölti fel a tudásbázist.

📁 Projektstruktúra
self_learning_rag_mvp/
├── core/
│   ├── views/
│   │   └── rag_views.py
│   ├── templates/
│   └── urls.py
├── knowledge/
│   ├── models.py
│   ├── admin.py
│   └── management/commands/
│       ├── seed_default_knowledge.py
│       ├── seed_poet_knowledge.py
│       └── seed_geo_knowledge.py
├── services/
│   ├── rag/
│   │   ├── rag_service.py
│   │   ├── prompt_builder.py
│   │   └── category_detector.py
│   ├── embedding/
│   └── ai_provider.py
└── templates/

🎯 Miért jó ez a projekt?

Kis méretű, de valós RAG rendszer

Könnyen bővíthető vállalati rendszerekhez

Oktatásra és kísérletezésre tökéletes

Külön modulokba szedett logika

Átlátható és tiszta architektúra

Alap fejlesztői template RAG-alapú alkalmazásokhoz

📘 Tervek / roadmap

 ElasticSearch integráció (vector search)

 Streaming LLM válaszok

 RAG finomhangolási eszközök

 Metaadat-szintű chunk filtering

 Admin UI a chunkok és embeddingek újragenerálásához

🏁 Licence

MIT — szabadon használható tanuláshoz és fejlesztéshez.