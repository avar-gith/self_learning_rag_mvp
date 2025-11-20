#file: knowledge/management/commands/seed_geography_knowledge.py
# Alap földrajzi témájú tudáselemek feltöltése a tudásbázisba.
# A tartalmak hosszabb, oktatási célú szövegek, hogy több chunk jöhessen létre.

from django.core.management.base import BaseCommand
from knowledge.models import KnowledgeCategory, KnowledgeItem


class Command(BaseCommand):
    help = "Kibővített földrajz témájú tudáselemek betöltése a 'Földrajz' kategóriába."

    # ----------------------------------------------------------------------
    def _create_or_get_category(self):
        """
        Létrehozza vagy lekéri a 'Földrajz' kategóriát.
        """
        category, was_created = KnowledgeCategory.objects.get_or_create(
            name="Földrajz",
            defaults={
                "description": (
                    "Középiskolai és általános földrajzi jelenségek, "
                    "földtani folyamatok, éghajlati rendszerek és kontinensek részletes leírása."
                )
            }
        )

        if was_created:
            self.stdout.write(self.style.SUCCESS("✔ 'Földrajz' kategória létrehozva."))
        else:
            self.stdout.write("ℹ 'Földrajz' kategória már létezik.")

        return category

    # ----------------------------------------------------------------------
    def _get_extended_geography_items(self):
        """
        Földrajz témájú hosszabb, több chunkra bontható tudáselemek listája.
        Minden elem (title, content) formátumban tér vissza.
        """
        return [
            (
                "A kőzetek fő típusai",
                """
A Föld szilárd kérge különböző kőzetekből áll, amelyek három nagy csoportba sorolhatók: 
üledékes, magmás és metamorf kőzetek.

**Üledékes kőzetek** akkor keletkeznek, amikor apró szemcsék, törmelékek vagy szerves maradványok rétegekben felhalmozódnak, 
majd hosszú idő alatt összecementálódnak. Ilyen például a homokkő, a mészkő vagy a konglomerátum. 
Ezek nagyon gyakran fosszíliákat tartalmaznak, ezért fontos forrásai a földtörténeti kutatásoknak.

**Magmás kőzetek** a Föld mélyéből származó olvadt kőzetanyag, a magma kihűlésével keletkeznek. 
A lassú lehűlés esetén nagy kristályok alakulnak ki (gránit), míg a gyors lehűlés apró kristályokat eredményez 
(bazalt). A magmás kőzetek a Föld kérgének egyik alapvető alkotói.

**Metamorf kőzetek** akkor jönnek létre, amikor meglévő kőzetek nagy nyomás vagy hő hatására átalakulnak. 
A palásodás, valamint az ásványi összetevők átrendeződése is jellemző lehet. Ide tartozik például a gneisz és a márvány.

A kőzetek vizsgálata fontos a földtani folyamatok megértésében és a természeti erőforrások feltárásában.
                """,
            ),
            (
                "A vulkánok működése",
                """
A vulkánok olyan földtani képződmények, ahol a felszín alatti magma a felszínre jut. 
A vulkánkitörés folyamata összetett: a Föld mélyén található magma a benne oldott gázok miatt nyomást gyakorol, 
és ha megfelelő repedés vagy gyenge zóna adódik, a felszín felé tör.

A vulkánoknak több típusa létezik: pajzsvulkánok, rétegvulkánok és hasadékvulkánok. 
A pajzsvulkánok (például Hawaii) alacsony viszkozitású lávát produkálnak, ezért széles, lapos formájuk van. 
A rétegvulkánok (mint a Vezúv) robbanásos kitöréseik miatt veszélyesek, mivel a magas viszkozitású magma 
gázcsapdákat képezhet, amelyek hirtelen, erőteljes robbanásokhoz vezetnek.

A vulkáni tevékenység alakítja a felszínt, termékeny talajt hoz létre, ugyanakkor komoly veszélyt jelenthet 
a lakosságra, például pyroklasztikus áramlások vagy lávafolyások révén.
                """,
            ),
            (
                "Éghajlati övezetek",
                """
A Föld éghajlata a napsugárzás eloszlásának köszönhetően több nagy övezetre osztható. 
Az éghajlati övezetek meghatározásában a földrajzi szélesség, a hőmérséklet és a csapadékeloszlás játszik kulcsfontosságú szerepet.

**Forró övezet**: Az Egyenlítő környékén található, egész évben magas hőmérséklet jellemzi. 
Ide tartoznak az esőerdők, a szavannák és az egyenlítői monszun területek.

**Mérsékelt övezet**: Két részre osztható: a meleg- és a hideg mérsékelt övezetre. 
A négy évszak jellemző, és itt található a legtöbb lakott terület. Magyarország is a mérsékelt övezet része.

**Hideg övezet**: A sarkvidékeken helyezkedik el, ahol az év nagy részében alacsony hőmérséklet és kevés csapadék van. 
A tundra és a jégsivatag ezekre a területekre jellemző.

Az éghajlati övezetek ismerete fontos a mezőgazdaság, a környezetvédelem és a klímaváltozás megértése szempontjából.
                """,
            ),
            (
                "Európa domborzata",
                """
Európa rendkívül változatos domborzattal rendelkezik, amely jelentős hatással van az éghajlatra, 
a népesség eloszlására és a gazdasági tevékenységekre.

A kontinens északi részén találhatók a Skandináv-hegység ősi, lekopott vonulatai. 
A középső területek túlnyomórészt alföldiek, mint a Német-alföld vagy a Lengyel-alföld. 
A domborzat déli irányban egyre magasabb: itt húzódnak Európa legnagyobb hegységei, 
például az Alpok, a Pireneusok, a Kárpátok és a Dinári-hegység.

Közép-Európában a Kárpát-medence jellegzetes földrajzi tájegység, amelyet a Kárpátok íve ölel körül. 
Magyarország nagy része alföldi jellegű, de megtalálhatók dombságok és középhegységek is, mint a Mátra és a Bükk.

Európa domborzata hozzájárul a kulturális sokszínűséghez, az eltérő gazdasági régiók kialakulásához és a történelmi fejlődéshez.
                """,
            ),
            (
                "A víz körforgása",
                """
A víz körforgása a Föld egyik legfontosabb természeti folyamata, amely a hidroszféra, a légkör és a litoszféra között zajlik. 
A körforgás a napsugárzás energiáján alapul.

A folyamat fő lépései:  
1. **Párolgás** – a víz a tengerekből, tavakból és talajból a légkörbe kerül.  
2. **Kondenzáció** – a lehűlt vízgőzből felhők alakulnak ki.  
3. **Csapadék** – a felhőkben lévő vízcseppek vagy jégkristályok lehullanak eső, hó vagy jégeső formájában.  
4. **Lefolyás és beszivárgás** – a víz visszakerül a felszín alatti és felszíni vizekbe.

A víz körforgása szabályozza a Föld éghajlatát, támogatja az élővilág fennmaradását, 
és kulcsfontosságú az emberi tevékenységek – például mezőgazdaság, ivóvízellátás – szempontjából.
                """,
            ),
        ]

    # ----------------------------------------------------------------------
    def handle(self, *args, **kwargs):
        """
        Fő parancs: kategória létrehozása + tudáselemek felvétele.
        """
        category = self._create_or_get_category()
        geography_items = self._get_extended_geography_items()

        created_item_count = 0

        for title, content in geography_items:
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
            self.style.SUCCESS(f"\n✓ Kész! {created_item_count} új földrajz tudáselem hozzáadva.")
        )
