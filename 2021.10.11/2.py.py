import json

with open("winners_data.json", "w") as write_file:
    json.dump([{'name': 'abc' , 'points': 100 }], write_file )
    #json.dump({'name': 'bc' , 'points': 10 }, write_file )


with open("winners_data.json", "r") as write_file:
    loaded = json.load(write_file)



loaded.append( {'name': 'bc' , 'points': 10})

print(loaded)
