var = [
        {
          "biome": "minecraft:nether_wastes",
          "parameters": {
            "temperature": 0,
            "humidity": 0,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0
          }
        },
        {
          "biome": "minecraft:soul_sand_valley",
          "parameters": {
            "temperature": 0,
            "humidity": -0.5,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0
          }
        },
        {
          "biome": "minecraft:crimson_forest",
          "parameters": {
            "temperature": 0.4,
            "humidity": 0,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0
          }
        },
        {
          "biome": "minecraft:warped_forest",
          "parameters": {
            "temperature": 0,
            "humidity": 0.5,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0.375
          }
        },
        {
          "biome": "minecraft:basalt_deltas",
          "parameters": {
            "temperature": -0.5,
            "humidity": 0,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0.175
          }
        }
      ]

var2 = [
        {
          "biome": "minecraft:nether_wastes",
          "parameters": {
            "temperature": -1000,
            "humidity": 19999,
            "continentalness": 9999990,
            "erosion": 99999999999,
            "weirdness": 10000000000000000,
            "depth": 9999999999,
            "offset": 99999999999
          }
        },
        {
          "biome": "minecraft:soul_sand_valley",
          "parameters": {
            "temperature": 0,
            "humidity": -0.5,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0
          }
        },
        {
          "biome": "minecraft:crimson_forest",
          "parameters": {
            "temperature": 0.4,
            "humidity": 0,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0
          }
        },
        {
          "biome": "minecraft:warped_forest",
          "parameters": {
            "temperature": 0,
            "humidity": 0.5,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0.375
          }
        },
        {
          "biome": "minecraft:basalt_deltas",
          "parameters": {
            "temperature": -0.5,
            "humidity": 0,
            "continentalness": 0,
            "erosion": 0,
            "weirdness": 0,
            "depth": 0,
            "offset": 0.175
          }
        }
      ]
import json
def write_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return True

names = []
for i in var:
    names.append(i["biome"])
print("done1")
for i in var2:
    names.append(i["biome"])
print("done2")
write_json_file("henk.json", names)
print("written")
print("gotta go for ")
var3 = json.load(open("biomes.json"))
for i in range(len(var3)):
    if i % 100 == 0:
        print(f"done with {i} out of {len(var3)}")
    names.append(var3[i]["biome"])
print("done3")

write_json_file("henk.json", names)
