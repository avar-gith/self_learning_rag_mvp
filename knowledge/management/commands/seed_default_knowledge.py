#file: knowledge/management/commands/seed_default_knowledge.py
# Alap fizika témájú tudáselemek feltöltése a tudásbázisba.

from django.core.management.base import BaseCommand
from knowledge.models import Category, KnowledgeItem


class Command(BaseCommand):
    help = "Alap fizika témájú tudáselemek betöltése a 'Fizika' kategóriába."

    def handle(self, *args, **kwargs):
        # ------------------------------------------------------------------
        # Fizika kategória létrehozása vagy lekérése
        # ------------------------------------------------------------------
        category, created = Category.objects.get_or_create(
            name="Fizika",
            defaults={"description": "Általános fizikai jelenségek, fogalmak és elméletek."}
        )

        if created:
            self.stdout.write(self.style.SUCCESS("✔ 'Fizika' kategória létrehozva."))
        else:
            self.stdout.write("ℹ 'Fizika' kategória már létezik.")

        # ------------------------------------------------------------------
        # 10 teszt tudáselem
        # ------------------------------------------------------------------
        physics_items = [
            ("Newton törvényei", "A klasszikus mechanika három alapvető törvénye, amelyek a mozgást írják le."),
            ("Relativitáselmélet", "Einstein elmélete a téridőről, amely a speciális és általános relativitást foglalja magába."),
            ("Fénysebesség", "A vákuumban terjedő fény sebessége: 299 792 458 m/s."),
            ("Gravitáció", "A tömeggel rendelkező objektumok közötti vonzóerő, amely Einstein szerint a téridő görbülete."),
            ("Kvantummechanika", "A mikroszkopikus részecskék viselkedését leíró fizikai elmélet."),
            ("Fekete lyukak", "Olyan objektumok, amelyek gravitációs tere olyan erős, hogy még a fény sem képes elhagyni."),
            ("Atommodellek", "Az atom felépítését leíró különböző modellek, például Bohr- és kvantummechanikai modellek."),
            ("Foton", "A fény és más elektromágneses hullámok alapvető részecskéje."),
            ("Hullám-részecske kettősség", "A kvantummechanika egyik alapelve: a részecskék hullámként és részecskeként is viselkednek."),
            ("Standard Modell", "A részecskefizika jelenleg elfogadott elméleti keretrendszere."),
        ]

        created_count = 0

        for title, content in physics_items:
            item, was_created = KnowledgeItem.objects.get_or_create(
                title=title,
                defaults={
                    "content": content,
                    "category": category,
                    "is_active": True,
                }
            )

            if was_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + '{title}' létrehozva."))
            else:
                self.stdout.write(f"  - '{title}' már létezik, kihagyva.")

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Kész! {created_count} új fizika tudáselem hozzáadva.")
        )
