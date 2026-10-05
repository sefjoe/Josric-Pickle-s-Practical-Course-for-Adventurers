import json
from pathlib import Path

PATH = Path('Josric_Pickle_Practical_Course_for_Adventurers_5etools.json')
data = json.loads(PATH.read_text(encoding='utf-8'))
entries = data['adventureData'][0]['data'][0]['entries']

def get(name):
    return next(e for e in entries if e.get('name') == name)

def remove_named(entry, name):
    entry['entries'] = [x for x in entry.get('entries', []) if not (isinstance(x, dict) and x.get('name') == name)]

# Version bump
data['_meta']['sources'][0]['version'] = '1.5'

# ROOM 2 — actual book titles
r2 = get('Room 2: See, Think, Act')
remove_named(r2, 'The Six Books')
book_block = {
    'type': 'entries',
    'name': 'The Six Books',
    'entries': [
        {'type':'list','items':[
            '{@b Eye — {@i The Watchful Adventurer}}',
            '{@b Sword — {@i Problems Best Solved by Steel}}',
            '{@b Hand — {@i A Manual of Practical Methods}}',
            '{@b Head — {@i On Thought Before Action}}',
            '{@b Foot — {@i A Survey of Roads and Ruins}}',
            '{@b Heart — {@i Courage in the Face of Certain Doom}}'
        ]},
        'The symbols are the important clue. The titles make the shelf feel like a real collection and give the players concrete books to name, pull, inspect, or hand to one another.'
    ]
}
# Insert immediately after the sentence introducing the six books
idx = next(i for i,x in enumerate(r2['entries']) if isinstance(x,str) and x.startswith('Six distinctive books'))
r2['entries'].insert(idx+1, book_block)

# ROOM 3 — scannable door-description bullets
r3 = get('Room 3: The Unlocked Door')
remove_named(r3, 'Describe the Door')
door_desc = {
    'type':'entries','name':'Describe the Door','entries':[
        'Give the players the details in pieces rather than as one paragraph:',
        {'type':'list','items':[
            'The door itself is faced in dark steel and looks far heavier than the other doors in the course.',
            'Six different keyholes are arranged at different heights, none using the same shape of key.',
            'Three numbered combination dials sit in a brass plate near the center.',
            'Two recessed sliding bolts disappear into the stone wall on either side.',
            'A ring of faint arcane-looking runes circles the frame.',
            'A narrow inspection slot is covered by a tiny hinged plate.',
            'Several old scratches around the locks suggest that somebody has tried to pick them before.',
            'A completely ordinary brass handle sits at normal hand height. It is unobstructed.'
        ]},
        'The locks, dials, bolts, runes, and keys are misdirection. The handle works normally because the door is not locked.'
    ]
}
insert_at = next(i for i,x in enumerate(r3['entries']) if isinstance(x,str) and x.startswith('Everything in the library is normal except'))
r3['entries'].insert(insert_at+1, door_desc)

# LIBRARIAN — appearance and RAW action vocabulary
lib = get('Optional Room: The Librarian')
remove_named(lib, 'The Librarian')
remove_named(lib, 'RAW Actions the Librarian Can Take')
lib_profile = {
    'type':'entries','name':'The Librarian','entries':[
        'The guardian looks like an elderly elf librarian rendered in translucent amber script rather than flesh. Her silver hair is fixed in a severe bun, half-moon spectacles rest low on her nose, and slate-gray academic robes hang perfectly straight even though no wind touches them. At the edges of her body, letters occasionally loosen from the shape, drift like dust, and settle back into place. Her expression is patient, exacting, and faintly disappointed before anyone has even spoken.',
        'Her voice is low, dry, and precise. She never raises it. She addresses characters by surname if she can learn it, and calls obviously bad arguments “administratively insufficient.”',
        'For checks she initiates, use Intelligence 18 (+4), Wisdom 16 (+3), and Charisma 14 (+2). Treat Arcana and Investigation as +6 and Insight and Perception as +5.'
    ]
}
raw_actions = {
    'type':'entries','name':'RAW Actions the Librarian Can Take','entries':[
        'The Librarian does not need a combat stat block unless initiative somehow starts. If it does, use the normal 2024 action system rather than inventing special combat powers.',
        {'type':'list','items':[
            '{@b Search.} She can take the Search action and make Wisdom (Insight) to judge a speaker’s state of mind or Wisdom (Perception) to notice a concealed item, altered seal, or swapped document.',
            '{@b Study.} She can take the Study action and make Intelligence (Arcana) to examine magical credentials or Intelligence (Investigation) to inspect a note, signature, catalog record, cipher, or forgery.',
            '{@b Help.} Once the party is authorized, she can take the Help action to assist a character with appropriate library research.',
            '{@b Utilize.} She can take the Utilize action to operate the catalog drawers, desk mechanisms, keys, and other nonmagical library objects.',
            '{@b Dodge or Ready.} If threatened in initiative, she can Dodge or Ready an action normally.'
        ]},
        'The protective barrier is a property of the room, not an attack or a special combat action by the Librarian. It simply prevents violence from reaching her. She does not make attacks against the party.'
    ]
}
# Place profile after terrain setup, then raw actions before lesson
terrain_idx = next(i for i,x in enumerate(lib['entries']) if isinstance(x,dict) and x.get('name')=='Terrain Setup')
lib['entries'].insert(terrain_idx+1, lib_profile)
lesson_idx = next(i for i,x in enumerate(lib['entries']) if isinstance(x,str) and x.startswith('The lesson is exactly'))
lib['entries'].insert(lesson_idx, raw_actions)

# TEAMWORK — DCs, object AC/HP, and attacks
team = get('Optional Room: The Teamwork Doors')
remove_named(team, 'Suggested Checks and Object Statistics')
team_rules = {
    'type':'entries','name':'Suggested Checks and Object Statistics','entries':[
        'These numbers are defaults, not mandatory solutions. If a player describes a better approach, set a reasonable check or simply let it work.',
        {'type':'table','caption':'Teamwork Door Defaults','colLabels':['Element','Suggested Check','DC','If Attacked'], 'colStyles':['col-3','col-4','col-1','col-4'], 'rows':[
            ['Standard lock','Utilize Thieves’ Tools; Dexterity (Sleight of Hand)','15','Lock: AC 19, 5 HP'],
            ['Arcane seal','Study; Intelligence (Arcana) to understand, then a plausible Magic action to suppress','15','Crystal seal: AC 13, 10 HP'],
            ['Heavy lever','Strength (Athletics)','13','Iron mechanism: AC 19, 18 HP'],
            ['Delicate latch','Dexterity (Sleight of Hand)','13','Latch: AC 19, 5 HP'],
            ['Instruction panel','Study; Intelligence (Investigation)','13','Wooden panel: AC 15, 10 HP'],
            ['Sequence controls','No check if the correctly communicated sequence is entered','—','Control box: AC 15, 10 HP'],
            ['Final simultaneous mechanisms','Strength (Athletics) or Dexterity (Sleight of Hand), depending on the device','12 each','Mechanism: AC 19, 18 HP'],
            ['Reinforced door itself','Force/pry: Strength check or Carpenter’s Tools','20','Iron/steel door: AC 19, 27 HP']
        ]},
        'The AC values follow the 2024 object rules by material: crystal/glass AC 13, wood AC 15, iron/steel AC 19. The listed HP use resilient-object benchmarks. Objects are immune to Poison and Psychic damage.',
        'If the characters spend the attacks and damage to destroy a door outright, let that work. The linked mechanisms teach the intended lesson, but brute force is still a legitimate solution rather than a secretly forbidden one.'
    ]
}
# Insert before the lesson
lesson_idx = next(i for i,x in enumerate(team['entries']) if isinstance(x,str) and x.startswith('The lesson is:'))
team['entries'].insert(lesson_idx, team_rules)

# MIRROR ROOM — initiative tracker object
mir = get('Room 4: The Mirror Gallery')
remove_named(mir, 'Initiative Tracker: Standing Mirrors')
tracker_note = {
    'type':'entries','name':'Initiative Tracker: Standing Mirrors','entries':[
        'Add one {@creature Standing Mirror (Echo Source)|JPTC2026} to the 5eTools initiative tracker for each PC. Rename the tracker rows Mirror 1, Mirror 2, and so on, and give the matching Echo and physical standee the same number.',
        'The tracker entry exists only so you can record damage conveniently. For rules purposes each mirror is an object, not a creature.'
    ]
}
# Put after linked-mirror explanation
link_idx = next(i for i,x in enumerate(mir['entries']) if isinstance(x,str) and x.startswith('Each Echo is linked'))
mir['entries'].insert(link_idx+1, tracker_note)

# RECOVERY — describe mechanism with RAW healing spells
rec = get('Emergency Recovery')
rec['entries'] = [
    'Immediately after the Mirror Gallery, the party finds a waist-high brass-and-stone lectern built into the wall. Two handprints are inset into its top around a softly glowing crystal, and the plaque above it reads:',
    {'type':'quote','entries':['A lesson ends when something is learned, not when the student can no longer stand.']},
    {'type':'entries','name':'How the Station Works','entries':[
        'A character places a hand on the crystal and takes the Magic action. The station releases one stored 1st-level {@spell cure wounds} effect: the character regains 2d8 + 3 Hit Points. The station can be used repeatedly by that character until the character reaches at least 75 percent of their Hit Point maximum; after that, it stops responding to that character.',
        'This uses the normal healing rules: regained Hit Points are added to current Hit Points and cannot raise a creature above its Hit Point maximum. If a character is at 0 Hit Points, the first successful healing immediately restores Hit Points and therefore brings the character back to consciousness normally.',
        'If the course has left a character Blinded, Deafened, Paralyzed, or Poisoned, the station can also release one stored {@spell lesser restoration} effect for that character, ending one of those conditions. Other temporary course conditions end normally when their source ends.',
        'The station never restores spell slots, Rage, Action Surge, Bardic Inspiration, Channel Divinity, consumables, Hit Dice, or other expended class resources. It is magical healing, not a Short Rest or Long Rest.'
    ]},
    'Because the healing is rolled normally, the final use can put a character somewhat above 75 percent. That is intentional; do not reduce healing already rolled.'
]

# FINAL EXAM — role of each reflection + no mirror shortcut
finale = get('Final Exam: Josric Pickle')
# Replace the existing scaling table
for x in finale['entries']:
    if isinstance(x,dict) and x.get('caption')=='Final Encounter Scaling':
        x['colLabels'] = ['PCs','Start','End of Round 1','End of Round 2']
        x['rows'] = [
            ['3','Josric + 1 Martial Reflection','1 Book Mimic','—'],
            ['4','Josric + 1 Martial Reflection','2 Book Mimics','1 Magic Reflection'],
            ['5','Josric + 1 Martial Reflection','2 Book Mimics','1 Magic Reflection + 1 Book Mimic'],
            ['6','Josric + 1 Martial Reflection + 1 Support Reflection','3 Book Mimics','1 Magic Reflection']
        ]
remove_named(finale, 'Choosing the Reflections')
remove_named(finale, 'No Mirror Shortcut in the Final Exam')
choice = {
    'type':'entries','name':'Choosing the Reflections','entries':[
        {'type':'list','items':[
            '{@b Martial Reflection.} Default: Fighter. Alternatives: Barbarian, Monk, Paladin, Ranger, Rogue, Blood Hunter, Brute, or Skirmisher.',
            '{@b Magic Reflection.} Default: Wizard. Alternatives: Sorcerer, Warlock, Druid, Artificer, or Caster.',
            '{@b Support Reflection.} Default: Cleric. Alternatives: Bard or Support.'
        ]},
        'Choose the specific card before play when possible. Prefer a role that creates a different problem from the actual party rather than simply copying the strongest PC.'
    ]
}
no_cheat = {
    'type':'entries','name':'No Mirror Shortcut in the Final Exam','entries':[
        'Correct: the final Josric Reflections are not linked to physical standing mirrors. There are no mirror objects to smash in this encounter.',
        'They are direct magical projections of Josric and use the prepared Josric Reflection cards. Breaking a mirror from the earlier room cannot affect them.',
        'The intended shortcut in the finale is recognizing the real objective: defeating or forcing Josric to yield immediately ends every remaining Reflection and Mimic.'
    ]
}
# Place role guide after scaling, no-cheat after role guide
scale_idx = next(i for i,x in enumerate(finale['entries']) if isinstance(x,dict) and x.get('caption')=='Final Encounter Scaling')
finale['entries'].insert(scale_idx+1, choice)
finale['entries'].insert(scale_idx+2, no_cheat)

# Add tracker creature for mirrors if absent
monsters = data.setdefault('monster', [])
monsters[:] = [m for m in monsters if m.get('name') != 'Standing Mirror (Echo Source)']
monsters.append({
    'name':'Standing Mirror (Echo Source)',
    'source':'JPTC2026',
    'size':['M'],
    'type':'construct',
    'alignment':['U'],
    'ac':[11],
    'hp':{'average':10,'formula':'10'},
    'speed':{'walk':0},
    'str':10,'dex':1,'con':10,'int':1,'wis':1,'cha':1,
    'vulnerable':['bludgeoning'],
    'immune':['poison','psychic'],
    'trait':[
        {'name':'Object, Not a Creature','entries':['This initiative entry is only a damage tracker. For rules purposes the mirror is an object, not a creature. Effects that target only creatures do not affect it.']},
        {'name':'Linked Echo','entries':['When this mirror is destroyed, its linked Mirror Echo is destroyed immediately.']}
    ]
})

# Quick-reference additions
quick = get('DM Quick Reference')
remove_named(quick, 'New Table Aids')
quick['entries'].append({
    'type':'entries','name':'New Table Aids','entries':[
        'Room 2 book titles are printed in the room entry.',
        'Room 3 has a bullet-list door description for fast narration.',
        'The Librarian has a full appearance plus Search, Study, Help, Utilize, Dodge, and Ready guidance using 2024 actions.',
        'Teamwork mechanisms include suggested DCs plus RAW-style object AC/HP.',
        'Add one Standing Mirror (Echo Source) tracker row per PC in the Mirror Gallery.',
        'The recovery station uses stored Cure Wounds and Lesser Restoration effects rather than an unexplained healing percentage.',
        'Final Reflection order: Martial at start, Magic in the later wave, plus Support at the 6-player start. Final Reflections have no breakable mirror source.'
    ]
})

PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(',',':')), encoding='utf-8')

# README version/update
readme = Path('README.md')
if readme.exists():
    txt = readme.read_text(encoding='utf-8')
    txt = txt.replace('**v1.4**','**v1.5**')
    if '## v1.5 table-use additions' not in txt:
        txt += '\n\n## v1.5 table-use additions\n\n- Named books in Room 2\n- Bullet-list reinforced-door narration\n- Librarian appearance and 2024 RAW action guidance\n- Teamwork-room DCs and object AC/HP\n- Initiative-tracker entry for standing mirrors\n- Recovery station explained through Cure Wounds/Lesser Restoration\n- Martial/Magic/Support Reflection staging for the final exam\n- Explicitly no breakable-mirror shortcut in the final exam\n'
    readme.write_text(txt, encoding='utf-8')

print('v1.5 update applied')
