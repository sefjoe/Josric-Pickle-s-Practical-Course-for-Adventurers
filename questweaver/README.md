# Questweaver conversion experiment — Josric v1.21

This is a separate experimental export from https://github.com/sefjoe/Josric-Pickle-s-Practical-Course-for-Adventurers/blob/main/Josric_Pickle_Practical_Course_for_Adventurers_5etools.json (SHA 6ce94eeb7b6d1ee7399b93a597b494a6318554cd); **main and the authoritative JSON are unchanged**.

## Files
- Josric_v1.21_Questweaver_Compendium.xml — all 40 custom source monster entries, including mirror variants and the Standing Mirror object-as-tracker. This follows the Fight Club/Game Master 5 compendium structure already proven to import into Questweaver in the earlier test. Action/bonus action and dice notation are converted from 5etools inline tags. **Actual Questweaver import of this new large file has not yet been verified.**
- Josric_v1.21_Adventure_Reference.md — readable adventure scene notes; NOT importable into Questweaver as an adventure.

## Test
In Questweaver on Android go Home > Settings > Content > Import XML Compendium, choose the XML file, then search Compendium for Book Mimic, Mirror Barbarian, Arcane Librarian, and Standing Mirror (Echo Source). Check attacks/traits and Add to Encounter.

## Outstanding
Importing a complete Game Master 5 campaign as scenes/encounters is not verified. The currently observed import menu says **Import XML Compendium**, not Import Campaign. The developer's website mentions campaigns, but published June 2026 statements called that functionality planned. Do not import the readable MD file as if it were campaign data. We should inspect the Adventures screen for a separate campaign import option.
