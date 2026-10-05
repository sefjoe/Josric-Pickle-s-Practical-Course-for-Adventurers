import copy
import json
from pathlib import Path

PATH = Path("Josric_Pickle_Practical_Course_for_Adventurers_5etools.json")
SOURCE = "JPTC2026"

with PATH.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Metadata
for src in data.get("_meta", {}).get("sources", []):
    if src.get("json") == SOURCE:
        src["version"] = "1.8"
data.setdefault("_meta", {})["dateLastModified"] = 1791237374

root_entries = data["adventureData"][0]["data"][0]["entries"]

def section_by_id(section_id):
    return next(x for x in root_entries if isinstance(x, dict) and x.get("id") == section_id)

def named_entry(entries, name):
    return next((x for x in entries if isinstance(x, dict) and x.get("name") == name), None)

# -----------------------------------------------------------------------------
# Librarian encounter: replace the old barrier-only handling with an actual
# initiative-ready creature and explicit table procedure.
# -----------------------------------------------------------------------------
lib = section_by_id("009")
old = lib["entries"]
image = next(x for x in old if isinstance(x, dict) and x.get("type") == "image")
terrain = named_entry(old, "Terrain Setup")
appearance = named_entry(old, "The Librarian")
appearance["entries"] = [
    "The guardian looks like an elderly elf librarian rendered in translucent amber script rather than flesh. Her silver hair is fixed in a severe bun, half-moon spectacles rest low on her nose, and slate-gray academic robes hang perfectly straight even though no wind touches them. At the edges of her body, letters occasionally loosen from the shape, drift like dust, and settle back into place. Her expression is patient, exacting, and faintly disappointed before anyone has even spoken.",
    "Her voice is low, dry, and precise. She never raises it. She addresses characters by surname if she can learn it, and calls obviously bad arguments ‘administratively insufficient.’",
    "Use {@creature Arcane Librarian|JPTC2026} for any checks or initiative. Her key mental abilities are Intelligence 18, Wisdom 16, and Charisma 14; Arcana, History, and Investigation are +6, while Insight and Perception are +5."
]

lib["entries"] = [
    image,
    terrain,
    appearance,
    "This room is optional and exists as a pacing reserve. Skip it when the session is running long; use it when the group is ahead.",
    "A magical Librarian blocks passage and states that the party is not authorized to enter the restricted collection.",
    {"type": "quote", "entries": ["State your authorization."]},
    "The Librarian cares about authorization, order, and protecting the collection. The simplest solution is Josric's original note, which counts as adequate authorization.",
    "Persuasion, Deception, Intimidation, exploiting bureaucracy, forged credentials, or another plausible social approach can work. Do not roll when the evidence or argument obviously satisfies what the Librarian wants. If a roll is useful, DC 13 is a suggested default; DC 15 is appropriate only for a thin or risky argument.",
    "Use {@creature Arcane Librarian|JPTC2026} as a normal initiative-tracker creature if initiative starts. She is immune to all damage and does not make damaging attacks.",
    "If a character attacks her, resolve the attack normally against AC 15. The attack can hit. On a hit, the Librarian takes 0 damage. The first time this happens, say: ‘That hits. As you strike the Librarian… nothing happens.’",
    {"type": "quote", "entries": ["Violence is not an accepted form of identification."]},
    {"type": "entries", "name": "Running the Librarian in Initiative", "entries": [
        "Roll initiative normally and add {@creature Arcane Librarian|JPTC2026} to the tracker. The joke works because she participates in initiative while remaining entirely unconcerned by attempts to damage her.",
        {"type": "list", "items": [
            "{@b Search.} She can use Search to notice concealed items, altered seals, swapped documents, or suspicious behavior.",
            "{@b Examine Credentials.} She can inspect a note, signature, magical mark, catalog record, cipher, forgery, or other claimed authorization.",
            "{@b Mage Hand.} She can retrieve books, accept paperwork, return misplaced objects, or silently move something a visitor should stop touching.",
            "{@b Prestidigitation.} She can clean surfaces, extinguish unattended flames, mark misplaced books, or produce small signs of administrative disapproval.",
            "{@b Utilize.} She can operate catalog drawers, desk mechanisms, keys, and other appropriate library objects.",
            "{@b Return to Shelf.} As a bonus action, she can magically move an unattended book or similar Tiny object toward its proper place.",
            "{@b Protect the Collection.} As a reaction, she can grant a threatened library object +5 AC against the triggering attack."
        ]},
        "Her all-damage immunity is part of her stat block. There is no separate force-field rule preventing attacks from connecting; attacks can hit her and simply deal no damage."
    ]},
    "The lesson is exactly: {@b A good adventurer learns what someone wants before deciding what to say.}",
    "This optional room contains no required Lesson Marker."
]

# -----------------------------------------------------------------------------
# Final Exam Reflections: make each a complete final-fight stat block.
# -----------------------------------------------------------------------------
monsters = data.setdefault("monster", [])
monster_by_name = {m.get("name"): m for m in monsters}
reflection_specs = [
    ("Barbarian", "Martial"), ("Fighter", "Martial"), ("Monk", "Martial"),
    ("Paladin", "Martial"), ("Ranger", "Martial"), ("Rogue", "Martial"),
    ("Blood Hunter", "Martial"), ("Brute", "Martial"), ("Skirmisher", "Martial"),
    ("Wizard", "Magic"), ("Sorcerer", "Magic"), ("Warlock", "Magic"),
    ("Druid", "Magic"), ("Artificer", "Magic"), ("Caster", "Magic"),
    ("Cleric", "Support"), ("Bard", "Support"), ("Support", "Support"),
]

for cls, role in reflection_specs:
    mirror_name = f"Mirror {cls}"
    reflection_name = f"Josric Reflection — {cls}"
    mirror = monster_by_name.get(mirror_name)
    ref = monster_by_name.get(reflection_name)
    if ref is None:
        if mirror is None:
            raise RuntimeError(f"Missing source mirror block for {cls}")
        ref = copy.deepcopy(mirror)
        ref["name"] = reflection_name
        monsters.append(ref)
        monster_by_name[reflection_name] = ref
    if mirror is not None:
        hp = int(mirror["hp"]["average"]) + 6
        ref["hp"] = {"average": hp, "formula": str(hp)}
    traits = [t for t in ref.get("trait", []) if t.get("name") not in {"Linked Mirror", "Reflected Form", "Josric's Reflection", "Final Exam Projection"}]
    for t in traits:
        if t.get("name") == "Published Chassis":
            t["entries"] = [e.replace("This Echo", "This Reflection").replace("This echo", "This reflection") if isinstance(e, str) else e for e in t.get("entries", [])]
        if t.get("name") == "Training Restraint":
            t["entries"] = ["The reflection does not attack an unconscious creature."]
    traits.insert(1 if traits else 0, {
        "name": "Final Exam Projection",
        "entries": [
            f"This is a {role.lower()} Reflection created directly by Josric Pickle. It uses the complete final-fight statistics printed here, including its increased hit points. It is not linked to a physical mirror, and destroying a mirror cannot harm it."
        ]
    })
    ref["trait"] = traits

# -----------------------------------------------------------------------------
# Arcane Librarian stat block.
# -----------------------------------------------------------------------------
all_damage_types = [
    "acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic",
    "piercing", "poison", "psychic", "radiant", "slashing", "thunder"
]
arcane_librarian = {
    "name": "Arcane Librarian",
    "source": SOURCE,
    "page": 0,
    "size": ["M"],
    "type": "construct",
    "alignment": ["U"],
    "ac": [15],
    "hp": {"average": 45, "formula": "6d8 + 18"},
    "speed": {"walk": 30},
    "str": 10,
    "dex": 12,
    "con": 16,
    "int": 18,
    "wis": 16,
    "cha": 14,
    "save": {"int": "+6", "wis": "+5"},
    "skill": {"arcana": "+6", "history": "+6", "insight": "+5", "investigation": "+6", "perception": "+5"},
    "immune": all_damage_types,
    "conditionImmune": ["charmed", "exhaustion", "frightened", "poisoned"],
    "senses": ["darkvision 60 ft."],
    "passive": 15,
    "languages": ["Common", "Draconic", "Elvish", "understands any written language contained in Josric's library"],
    "cr": "0",
    "trait": [
        {"name": "Library Authorization", "entries": ["The Librarian recognizes genuine written or magical authorization from Josric Pickle. Presenting valid authorization satisfies her demand automatically; no ability check is required."]},
        {"name": "Indestructible Custodian", "entries": ["The Librarian is immune to all damage. Attacks and damaging effects are still resolved normally. An attack can hit her Armor Class, but any damage dealt to her is reduced to 0."]},
        {"name": "Constructed Purpose", "entries": ["The Librarian doesn't require air, food, drink, or sleep."]}
    ],
    "action": [
        {"name": "Search", "entries": ["The Librarian takes the Search action, using Wisdom (Perception) or Wisdom (Insight) as appropriate."]},
        {"name": "Examine Credentials", "entries": ["The Librarian examines one document, insignia, magical mark, or other claimed proof of authorization she can see within 5 feet. She recognizes genuine authorization from Josric automatically. A forgery or misleading document can be contested by the Librarian's Intelligence (Investigation) or Wisdom (Insight), as appropriate."]},
        {"name": "Mage Hand", "entries": ["The Librarian casts {@spell mage hand} without material components. She normally uses it to retrieve books, accept paperwork, return misplaced objects, or point toward something a visitor should stop touching."]},
        {"name": "Prestidigitation", "entries": ["The Librarian casts {@spell prestidigitation} without material components. She normally uses it to clean surfaces, extinguish unattended flames, mark misplaced books, or produce small signs of disapproval."]},
        {"name": "Utilize", "entries": ["The Librarian takes the Utilize action to operate a library mechanism, open or close an authorized door, retrieve a record, or manipulate another appropriate object."]}
    ],
    "bonus": [
        {"name": "Return to Shelf", "entries": ["One unattended book or similar Tiny object the Librarian can see within 30 feet magically moves up to 20 feet toward its proper location. This ability can't move an object being worn or carried by an unwilling creature."]}
    ],
    "reaction": [
        {"name": "Protect the Collection", "entries": ["When a creature the Librarian can see within 30 feet makes an attack against a book, shelf, desk, manuscript, or other library property, the Librarian grants that object a +5 bonus to AC against the triggering attack."]}
    ]
}
# Replace if it already exists; otherwise insert before Josric for easy browsing.
monsters[:] = [m for m in monsters if m.get("name") != "Arcane Librarian"]
josric_index = next((i for i, m in enumerate(monsters) if m.get("name") == "Josric Pickle"), len(monsters))
monsters.insert(josric_index, arcane_librarian)

# -----------------------------------------------------------------------------
# Final Exam staging and direct links to actual final-fight stat blocks.
# -----------------------------------------------------------------------------
finale = section_by_id("014")
scaling = next(x for x in finale["entries"] if isinstance(x, dict) and x.get("caption") == "Final Encounter Scaling")
scaling["rows"] = [
    ["3", "Josric + 1 Martial Reflection (default: {@creature Josric Reflection — Fighter|JPTC2026})", "1 Book Mimic", "—"],
    ["4", "Josric + 1 Martial Reflection (default: {@creature Josric Reflection — Fighter|JPTC2026})", "2 Book Mimics", "1 Magic Reflection (default: {@creature Josric Reflection — Wizard|JPTC2026})"],
    ["5", "Josric + 1 Martial Reflection (default: {@creature Josric Reflection — Fighter|JPTC2026})", "2 Book Mimics", "1 Magic Reflection (default: {@creature Josric Reflection — Wizard|JPTC2026}) + 1 Book Mimic"],
    ["6", "Josric + 1 Martial Reflection (default: {@creature Josric Reflection — Fighter|JPTC2026}) + 1 Support Reflection (default: {@creature Josric Reflection — Cleric|JPTC2026})", "3 Book Mimics", "1 Magic Reflection (default: {@creature Josric Reflection — Wizard|JPTC2026})"]
]
choosing = named_entry(finale["entries"], "Choosing the Reflections")
choosing["entries"] = [
    {"type": "list", "items": [
        "{@b Martial Reflection.} Default: {@creature Josric Reflection — Fighter|JPTC2026}. Alternatives: {@creature Josric Reflection — Barbarian|JPTC2026}, {@creature Josric Reflection — Monk|JPTC2026}, {@creature Josric Reflection — Paladin|JPTC2026}, {@creature Josric Reflection — Ranger|JPTC2026}, {@creature Josric Reflection — Rogue|JPTC2026}, {@creature Josric Reflection — Blood Hunter|JPTC2026}, {@creature Josric Reflection — Brute|JPTC2026}, or {@creature Josric Reflection — Skirmisher|JPTC2026}.",
        "{@b Magic Reflection.} Default: {@creature Josric Reflection — Wizard|JPTC2026}. Alternatives: {@creature Josric Reflection — Sorcerer|JPTC2026}, {@creature Josric Reflection — Warlock|JPTC2026}, {@creature Josric Reflection — Druid|JPTC2026}, {@creature Josric Reflection — Artificer|JPTC2026}, or {@creature Josric Reflection — Caster|JPTC2026}.",
        "{@b Support Reflection.} Default: {@creature Josric Reflection — Cleric|JPTC2026}. Alternatives: {@creature Josric Reflection — Bard|JPTC2026} or {@creature Josric Reflection — Support|JPTC2026}."
    ]},
    "Use the Josric Reflection stat blocks, not the Mirror Echo stat blocks. Each Final Exam Reflection is a complete initiative-ready creature with its final-fight hit points already included. Do not add 6 HP at the table.",
    "Choose the specific card before play when possible. Prefer a role that creates a different problem from the actual party rather than simply copying the strongest PC."
]

# -----------------------------------------------------------------------------
# Quick references: add a complete Final Exam table and update DM aid text.
# -----------------------------------------------------------------------------
quick = section_by_id("015")
quick["entries"] = [x for x in quick["entries"] if not (isinstance(x, dict) and x.get("name") == "Final Exam Reflection Quick Reference")]
reflection_rows = []
for cls, role in reflection_specs:
    ref = monster_by_name[f"Josric Reflection — {cls}"]
    reflection_rows.append([cls, role, f"{{@creature Josric Reflection — {cls}|JPTC2026}}", str(ref["hp"]["average"])])
quick["entries"].append({
    "type": "entries",
    "name": "Final Exam Reflection Quick Reference",
    "entries": [
        "These are separate initiative-ready Final Exam creatures. Their listed hit points already include the +6 final-fight durability increase, and none has a Linked Mirror trait.",
        {"type": "table", "caption": "Initiative-Ready Final Exam Reflections", "colLabels": ["Reflection", "Role", "Use", "HP"], "colStyles": ["col-3", "col-2", "col-5", "col-2"], "rows": reflection_rows}
    ]
})

dm = section_by_id("017")
dm_list = next(x for x in dm["entries"] if isinstance(x, dict) and x.get("type") == "list")
dm_list["items"] = [i for i in dm_list["items"] if not i.startswith("Librarian:") and not i.startswith("Final Exam Reflections:")]
dm_list["items"].insert(3, "Librarian: use {@creature Arcane Librarian|JPTC2026}; AC 15, 45 HP, immune to all damage. Attacks can hit but deal 0 damage. If attacked, roll initiative; she never makes damaging attacks.")
dm_list["items"].insert(10, "Final Exam Reflections: use the separate Josric Reflection stat blocks, not Mirror Echoes. Their final HP is already printed and they have no Linked Mirror trait. Defaults are Fighter (Martial), Wizard (Magic), and Cleric (Support).")
new_aids = named_entry(dm["entries"], "New Table Aids")
new_aids["entries"] = [e for e in new_aids["entries"] if not e.startswith("The Librarian opens") and not e.startswith("Final Reflection order") and not e.startswith("Final Reflections split")]
new_aids["entries"].extend([
    "The Librarian opens with “State your authorization.” Use {@creature Arcane Librarian|JPTC2026} if initiative starts. She is immune to all damage; attacks can hit her but deal 0, and she continues handling books, credentials, and the collection instead of attacking back.",
    "Final Reflection order: Martial at start, Magic in the later wave, plus Support at the 6-player start. Defaults are Fighter, Wizard, and Cleric.",
    "Final Exam Reflections use separate initiative-ready Josric Reflection stat blocks with their increased HP already included. They split directly from Josric and have no breakable mirror source."
])

# -----------------------------------------------------------------------------
# Designer's Notes / design log.
# -----------------------------------------------------------------------------
design = section_by_id("018")
design["entries"] = [x for x in design["entries"] if not (isinstance(x, dict) and x.get("name") == "Design Log — v1.8: Initiative-Ready Creatures")]
log_entry = {
    "type": "entries",
    "name": "Design Log — v1.8: Initiative-Ready Creatures",
    "entries": [
        "I split the Final Exam Reflections into their own complete stat blocks instead of making myself remember ‘Mirror Echo +6 HP’ during play. The goal was table usability: every creature that can enter initiative should already be ready to run.",
        "The Final Exam Reflections deliberately do not have the Mirror Gallery shortcut. They come directly from Josric, so there is no physical mirror to destroy. The shortcut in the final fight is recognizing that defeating Josric ends the entire exam.",
        "I gave the Librarian a real initiative-ready stat block because players may decide to attack her even though the encounter is intended to be social.",
        "The Librarian is immune to all damage, but attacks against her still resolve normally and can hit. I specifically wanted the moment where I can say, ‘That hits. As you strike the Librarian… nothing happens.’",
        "She does not retaliate with damaging attacks. She continues doing her job in initiative—moving books, protecting the collection, examining credentials, and insisting on authorization.",
        "Her response to being attacked remains: ‘Violence is not an accepted form of identification.’",
        "The point of the Librarian's invulnerability is not to punish the players. It is a joke, a strong signal that violence is the wrong tool for this particular problem, and a way to keep the optional social encounter from becoming an unnecessary resource-draining combat."
    ]
}
insert_at = next((i + 1 for i, x in enumerate(design["entries"]) if isinstance(x, dict) and x.get("name") == "How the Finale Changed"), len(design["entries"]))
design["entries"].insert(insert_at, log_entry)

# Validate uniqueness and requirements.
names = [m.get("name") for m in monsters]
if len(names) != len(set(names)):
    dupes = sorted({n for n in names if names.count(n) > 1})
    raise RuntimeError(f"Duplicate monster names after update: {dupes}")
required = ["Arcane Librarian"] + [f"Josric Reflection — {cls}" for cls, _ in reflection_specs]
missing = [n for n in required if n not in names]
if missing:
    raise RuntimeError(f"Missing required creatures: {missing}")
for n in required[1:]:
    m = monster_by_name[n]
    if any(t.get("name") == "Linked Mirror" for t in m.get("trait", [])):
        raise RuntimeError(f"Final Reflection still has Linked Mirror: {n}")

with PATH.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    f.write("\n")

print("Updated to v1.8")
print("Arcane Librarian added")
print(f"Final Exam reflections ready: {len(reflection_specs)}")
