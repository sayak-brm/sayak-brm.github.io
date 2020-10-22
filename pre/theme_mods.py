import json

mods = json.load(open("pre/theme_mods/mods.json"))

for mod_fn in mods.keys():
    con = ""
    with open(mod_fn, 'r') as mod_file:
        con = mod_file.read()
    loc = con.find(mods[mod_fn][0])
    con = con[:loc+mods[mod_fn][2]] + mods[mod_fn][1] + con[loc+len(mods[mod_fn][1]):]
    with open(mod_fn, 'w') as mod_file:
        con = mod_file.write(con)
