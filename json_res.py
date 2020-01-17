import json

with open("./data/all_races.json") as file:
  data = json.load(file)
  for item in data:
    for i in (item.items()):
      print(i)