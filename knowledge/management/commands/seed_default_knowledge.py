#file: knowledge/management/commands/seed_default_knowledge.py
# Alap fizika témájú tudáselemek feltöltése a tudásbázisba.
# A tartalmak hosszabb, oktatási jellegű szövegek, hogy több chunk jöhessen létre.

from django.core.management.base import BaseCommand
from knowledge.models import KnowledgeCategory, KnowledgeItem


class Command(BaseCommand):
    help = "Kibővített fizika témájú tudáselemek betöltése a 'Fizika' kategóriába."

    # ----------------------------------------------------------------------
    def _create_or_get_category(self):
        """
        Létrehozza vagy lekéri a 'Fizika' kategóriát.
        """
        category, was_created = KnowledgeCategory.objects.get_or_create(
            name="Fizika",
            defaults={
                "description": (
                    "Középiskolai és általános fizikai jelenségek, fogalmak, "
                    "törvények és elméletek részletes magyarázata."
                )
            }
        )

        if was_created:
            self.stdout.write(self.style.SUCCESS("✔ 'Fizika' kategória létrehozva."))
        else:
            self.stdout.write("ℹ 'Fizika' kategória már létezik.")

        return category

    # ----------------------------------------------------------------------
    def _get_extended_physics_items(self):
        """
        Fizika témájú hosszabb, több chunkra bontható tudáselemek listája.
        Minden elem (title, content) formátumban tér vissza.
        """
        return [
            (
                "Newton törvényei",
                """
Isaac Newton három alapvető törvénye a klasszikus mechanika alapját képezi. 
Ezek a törvények a mozgás leírására, a testekre ható erőkre és azok kölcsönhatásaira vonatkoznak.

1. **Tehetetlenség törvénye**:  
   Egy test megtartja egyenes vonalú, egyenletes mozgását vagy nyugalmi állapotát mindaddig, amíg egy külső erő meg nem változtatja azt. 
   Ez az alapelv kimondja, hogy a mozgás természetes állapota nem a nyugalom, hanem az egyenletes mozgás.

2. **Dinamika alapegyenlete**:  
   A test gyorsulása egyenesen arányos a rá ható erővel és fordítottan arányos a tömegével: F = m * a.  
   Ez a törvény kapcsolatot teremt az erő és a mozgásállapot-változás között.

3. **Hatás-ellenhatás törvénye**:  
   Minden erőhatásnak van egy egyenlő nagyságú, ellentétes irányú ellenhatása. 
   Ez a törvény írja le a testek kölcsönhatását, például azt, hogy egy asztal miért tol vissza, amikor rányomjuk a kezünket.

Newton törvényei a modern fizika számos területén alapvető kiindulási pontot jelentenek.
                """,
            ),
            (
                "Relativitáselmélet",
                """
Einstein relativitáselmélete két részből áll: a speciális és az általános relativitásból. 
A speciális relativitás szerint a fény sebessége minden inerciarendszerben állandó, és a mozgó rendszerekben az idő lassabban telik.

A tömeg-energia ekvivalencia az elmélet egyik legismertebb következménye, melyet az E = mc² egyenlet fejez ki.

Az általános relativitáselmélet szerint a gravitáció nem erő, hanem a téridő görbülete. 
A nagy tömegű objektumok meggörbítik körülöttük a téridőt, és ez a görbület határozza meg a testek mozgását. 
A fekete lyukak, a gravitációs lencsehatás és a gravitációs hullámok mind ezen elmélet következményei.

Az elméletet számos kísérlet és csillagászati megfigyelés igazolja.
                """,
            ),
            (
                "Fekete lyukak",
                """
A fekete lyukak a téridő olyan extrém objektumai, amelyek gravitációs terük annyira erős, hogy még a fény sem képes elhagyni őket. 
Keletkezésük jellemzően nagytömegű csillagok életciklusának végállapota, amikor a mag összeomlik.

A fekete lyuknak három fő jellemzője van: tömeg, töltés és perdület. 
A Schwarzschild-sugár jelöli azt a határt (eseményhorizont), amelyen belül semmi sem menekülhet.

A fekete lyukak nem „szívnak be” mindent, hanem ugyanúgy gravitációs objektumok, mint bármely más tömeg, csak extrém módon. 
A Hawking-sugárzás elmélete szerint a fekete lyukak nagyon lassan párolognak is.

A galaxisok közepén szupermasszív fekete lyukak találhatók, amelyek több millió naptömegűek lehetnek.
                """,
            ),
            (
                "Hullám-részecske kettősség",
                """
A kvantummechanika egyik központi jelensége, hogy a részecskék egyszerre mutathatnak hullám- és részecsketulajdonságokat. 
Ez a kettősség a fény esetében régóta ismert (foton), de kiderült, hogy az elektronok, protonok és más anyagi részecskék is hullámként viselkedhetnek.

A kettősség legismertebb kísérlete a kettős rés kísérlet, amelyben az egyes részecskék interferenciamintázatot hoznak létre – még akkor is, ha egyenként lövik őket a résre. 
Ez azt sugallja, hogy a részecske „önmagával interferál”.

A jelenség megértése alapvető fontosságú a modern fizikában.
                """,
            ),
            (
                "Atommodellek fejlődése",
                """
Az atom szerkezetének megértése hosszú történelmi folyamat eredménye.

1. **Dalton modellje** 
   Az atomot oszthatatlan gömbként képzelte el.

2. **Thomson-féle mazsolás puding modell** 
   Az atom pozitív „masszából” áll, amelyben elektronok helyezkednek el.

3. **Rutherford modellje**
   A kísérletek szerint az atom nagy része üres tér, középen kicsi, pozitív maggal.

4. **Bohr modellje**
   Az elektronok meghatározott pályákon keringenek, energiájuk csak bizonyos szinteket vehet fel.

5. **Kvantummechanikai atommodell**
   Az elektron nem rendelkezik pontos pályával; valószínűségi felhőként írható le.

A modern modell adja a pontos leírást a kémiai kötések és a fizikai tulajdonságok megértéséhez.
                """,
            ),
        ]

    # ----------------------------------------------------------------------
    def handle(self, *args, **kwargs):
        """
        Fő parancs: kategória létrehozása + tudáselemek felvétele.
        """
        category = self._create_or_get_category()
        physics_items = self._get_extended_physics_items()

        created_item_count = 0

        for title, content in physics_items:
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
            self.style.SUCCESS(f"\n✓ Kész! {created_item_count} új fizika tudáselem hozzáadva.")
        )
