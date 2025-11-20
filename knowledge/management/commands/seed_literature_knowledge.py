#file: knowledge/management/commands/seed_literature_knowledge.py
# Alap irodalmi témájú tudáselemek feltöltése a tudásbázisba.
# A tartalmak hosszabb, oktatási célú szövegek, hogy több chunk jöhessen létre.

from django.core.management.base import BaseCommand
from knowledge.models import KnowledgeCategory, KnowledgeItem


class Command(BaseCommand):
    help = "Kibővített magyar irodalom témájú tudáselemek betöltése az 'Irodalom' kategóriába."

    # ----------------------------------------------------------------------
    def _create_or_get_category(self):
        """
        Létrehozza vagy lekéri az 'Irodalom' kategóriát.
        """
        category, was_created = KnowledgeCategory.objects.get_or_create(
            name="Irodalom",
            defaults={
                "description": (
                    "Klasszikus magyar irodalmi művek, szerzői életrajzok, "
                    "műelemzések és műfaji ismertetők részletes magyarázatokkal."
                )
            }
        )

        if was_created:
            self.stdout.write(self.style.SUCCESS("✔ 'Irodalom' kategória létrehozva."))
        else:
            self.stdout.write("ℹ 'Irodalom' kategória már létezik.")

        return category

    # ----------------------------------------------------------------------
    def _get_extended_literature_items(self):
        """
        Irodalom témájú hosszabb, több chunkra bontható tudáselemek listája.
        Minden elem (title, content) formátumban tér vissza.
        """
        return [
            (
                "Arany János élete és munkássága",
                """
Arany János a 19. századi magyar irodalom egyik legkiemelkedőbb alakja, a ballada műfajának mestere, 
Petőfi Sándor barátja és a magyar nyelv művészi megformálásának egyik legfontosabb alakja. 
Nagyszalontán született 1817-ben, szerény körülmények között. Tanulmányait részben önképzéssel végezte, 
mivel családja nem tudta folyamatosan támogatni.

Arany első nagy sikere a Toldi megjelenésével jött 1846-ban, amelyet Petőfi fedezett fel és támogatott. 
A Toldi trilógia máig a magyar epikus költészet egyik legfontosabb alkotása. Arany balladái, például a Szondi két apródja, 
A walesi bárdok vagy az Ágnes asszony, komplex szerkezetükkel, lélektani mélységükkel és tragikus hangulatukkal tűnnek ki.

Későbbi éveiben a Magyar Tudományos Akadémia főtitkára lett, és jelentős szerepet játszott a magyar irodalmi élet irányításában. 
Munkásságát a népköltészet iránti érdeklődés, a klasszicista formafegyelem és a romantikus érzésvilág ötvöződése jellemzi.
                """,
            ),
            (
                "Petőfi Sándor – János vitéz összefoglaló",
                """
A János vitéz Petőfi Sándor egyik legismertebb elbeszélő költeménye, amely 1845-ben jelent meg. 
A mű egy egyszerű juhászfiú, Kukorica Jancsi kalandjait mutatja be, aki szerelmét, Iluskát elveszíti, 
majd hősies tettek révén János vitézzé válik.

A történet bejárja a magyar falusi világot, a francia király udvarát, a sötét Óriások Földjét, 
és végül eljut a Tündérek Országába, ahol János vitéz újra találkozik Iluskával. 
A mű keveri a népmesei elemeket és a romantikus kalandmotívumokat, könnyen érthető nyelvezettel és élénk képekkel.

A János vitéz sokak szerint a magyar nemzeti identitás egyik fontos irodalmi alappillére, 
mivel a hűséget, a bátorságot, a szerelem erejét és az önfeláldozást középpontba állítja.
                """,
            ),
            (
                "A ballada műfaji jellemzői",
                """
A ballada a líra, az epika és a dráma műfajainak határán elhelyezkedő, tömör, sűrített kifejezésmódú műfaj. 
Legfőbb sajátossága, hogy egy tragikus, konfliktusos történetet mesél el, gyakran párbeszédekkel és gyors jelenetváltásokkal. 
A cselekmény előrehaladása sokszor szaggatott, a kihagyásos szerkesztés miatt a történet bizonyos részei kimaradnak, 
és az olvasónak kell kikövetkeztetnie az összefüggéseket.

A balladák hangulata általában komor, gyakran moralizáló vagy történelmi jellegű. 
Jellemző a refrén, a balladai homály és a végzet elkerülhetetlenségének érzete. 
A magyar irodalomban Arany János balladái számítanak a műfaj csúcsának, például: Ágnes asszony, V. László, A walesi bárdok.

A ballada műfaja kitűnő példa arra, hogyan lehet egy rövid terjedelemben rendkívül erős drámai hatást elérni.
                """,
            ),
            (
                "Jókai Mór – A kőszívű ember fiai",
                """
A kőszívű ember fiai Jókai Mór egyik legismertebb romantikus történelmi regénye, 
amely az 1848–49-es forradalom és szabadságharc idején játszódik. 
A történet középpontjában a Baradlay család áll, különösen a három fiú: Ödön, Richárd és Jenő.

A mű a romantika jellegzetes jegyeit viseli: érzelmes jelenetek, eszményített hősök, 
drámai fordulatok és történelmi háttér. Jókai nagy hangsúlyt fektet a családi szeretetre, 
a hazaszeretet eszméjére és az önfeláldozásra.

A regény sok szereplőt mozgat, és párhuzamos cselekményszálai jól tükrözik a magyar társadalom sokszínűségét a forradalom idején. 
A mű máig az iskolai tananyag része, és a magyar romantikus irodalom egyik legfontosabb darabja.
                """,
            ),
            (
                "A romantika irodalmi irányzat jellemzői",
                """
A romantika az irodalomtörténet egyik meghatározó korszaka, amely a 18–19. században terjedt el Európában, 
és erősen hatott a magyar irodalomra is. A romantika középpontjában az egyén, az érzelmek és a szabadságvágy áll.

A művekben hangsúlyos az erős érzelmi töltet, a hősies alakok, a természet misztikuma, 
az idealizálás és a nemzeti érzelmek megjelenítése. A romantikus hős gyakran kívülálló, 
aki a társadalmi normákkal szembekerülve küzd igazságáért.

Magyarországon a romantika kiemelkedő alakjai: Petőfi Sándor, Arany János, Jókai Mór és Vörösmarty Mihály. 
A korszak művei a mai napig a magyar kulturális identitás fontos alappillérei.
                """,
            ),
        ]

    # ----------------------------------------------------------------------
    def handle(self, *args, **kwargs):
        """
        Fő parancs: kategória létrehozása + tudáselemek felvétele.
        """
        category = self._create_or_get_category()
        literature_items = self._get_extended_literature_items()

        created_item_count = 0

        for title, content in literature_items:
            knowledge_item, was_created = KnowledgeItem.objects.get_or_create(
                title=title,
                defaults={
                    "content": content.strip(),
                    "category": category,
                    "is_active": True,
                }
            )

            if was_created:
                created_item_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + '{title}' létrehozva."))

            else:
                self.stdout.write(f"  - '{title}' már létezik, kihagyva.")

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Kész! {created_item_count} új irodalom tudáselem hozzáadva.")
        )
