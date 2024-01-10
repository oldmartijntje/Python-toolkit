# a function to read a json file
import json
import os
import random

def deepcopy(data):
    return parse_json(stringify_json(data))

def read_json_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def does_file_exist(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False

def write_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return True

def stringify_json(data):
    return json.dumps(data)

def parse_json(data):
    try:
        return json.loads(data)
    except Exception as e:
        print(f"Error parsing json: {e}")
        return data

def remove_last_quote(input_string):
    # Check if the last character is a double quote
    
    if input_string.endswith("\\\""):
        # Remove the last characters
        modified_string = input_string[:-2]
        return modified_string
    elif input_string.endswith('"'):
        # Remove the last character
        modified_string = input_string[:-1]
        return modified_string
    else:
        # Return the original string if the last character is not a double quote
        return input_string
    
def remove_first_quote(input_string):
    # Check if the first character is a double quote
    if input_string.startswith('"'):
        # Remove the first character
        modified_string = input_string[1:]
        return modified_string
    elif input_string.startswith("\\\""):
        # Remove the first characters
        modified_string = input_string[2:]
        return modified_string
    else:
        # Return the original string if the first character is not a double quote
        return input_string
    
def checkForPureString(output, find, randomValue):
    first = remove_last_quote(output.split(find, 1)[0])
    if first != output.split(find, 1)[0]:
        second = remove_first_quote(output.split(find, 1)[1])
        output = first + str(randomValue) + second
    else:
        output = output.split(find, 1)[0] + str(randomValue) + output.split(find, 1)[1]
    return output

def getRandomFromData(data, typeOfData):
    if type(data) is list:
        return data[random.randint(0, len(data) - 1)]
    elif type(data) is dict:
        if 'unique' in data and data['unique'] == True and 'uniqueIdentifier' in data:
            if data["uniqueIdentifier"] in used:
                if type(used[data["uniqueIdentifier"]]) is str:
                    used[data["uniqueIdentifier"]] = used[data["uniqueIdentifier"]] + "1"
                elif type(used[data["uniqueIdentifier"]]) is float:
                    used[data["uniqueIdentifier"]] = used[data["uniqueIdentifier"]] + 0.1
                else:
                    used[data["uniqueIdentifier"]] += 1
            else:
                if 'min' in data:
                    used[data["uniqueIdentifier"]] = data['min']
                elif typeOfData == 'float':
                    used[data["uniqueIdentifier"]] = 0.1
                else:
                    used[data["uniqueIdentifier"]] = 0
            return used[data["uniqueIdentifier"]]
        elif 'min' in data and 'max' in data:
            if typeOfData == 'float':
                return random.uniform(data['min'], data['max'])
            else:
                return random.randint(data['min'], data['max'])
        elif 'min' in data:
            if typeOfData == 'float':
                return random.uniform(data['min'], 100)
            else:
                return random.randint(data['min'], 100.001)
        elif 'max' in data:
            if typeOfData == 'float':
                return random.uniform(0, data['max'])
            else:
                return random.randint(0.1, data['max'])
        elif typeOfData == 'json':
            return stringify_json(data)
        else:
            return data
    else:
        return data
    
def getValue(selectedData, output):
    randomValue = getRandomFromData(selectedData['value'], selectedData['type'])
    match selectedData['type']:
        case 'string':
            output = output.split(find, 1)[0] + str(randomValue) + output.split(find, 1)[1]
        case 'int':
            output = checkForPureString(output, find, randomValue)
        case 'float':
            output = checkForPureString(output, find, randomValue)
        case 'bool':
            output = checkForPureString(output, find, str(randomValue).lower())
        case 'json':
            output = checkForPureString(output, find, randomValue)
    return output

output = {}
used = {}
fileName = 'input.json'
exportFileName = 'output.json'

defaultValues = {
    "firstName": {
        "type": "string",
        "value": [
            "John", "Jane", "Jack", "Jill", "Jim", "Jenny", "Joe", "Jill", "Jesse", "Jasmine", "Martijn", "Martin", "Emiel", "Donald", "Thomas", 
            "Tom", "Tim", "Tina", "Timo", "Tijmen", "Tijl", "Robbie", "David"
        ]
    },
    "lastName": {
        "type": "string",
        "value": [
            "Trump", "Biden", "Obama", "Clinton", "Bush", "Johnson", "Kennedy", "Roosevelt", "Lincoln", "Washington", "Adams", "Jefferson",
            "Madison", "Monroe", "Jackson", "Van Buren", "Harrison", "Tyler", "Polk", "Taylor", "Fillmore", "Pierce", "Buchanan", "Lincoln",
            "Johnson", "Grant", "Hayes", "Garfield", "Arthur", "Cleveland", "Harrison", "McKinley", "Roosevelt", "Taft", "Wilson", "Harding",
            "Van-Haren", "De_Vries", "Koman", "Van_Dijk", "Bakker", "Janssen", "Visser", "Smit", "Meijer", "De Boer", "Mulder", "De_Groot",
        ]
    },
    "digit": {
        "type": "int",
        "value": {
            "min": 0,
            "max": 9
        }
    },
    "stringDigit": {
        "type": "string",
        "value": {
            "min": 0,
            "max": 9
        }
    },
    "id": {
        "type": "int",
        "value": {
            "unique": True,
            "uniqueIdentifier": "id"
        }
    },
    "lowerChar": {
        "type": "string",
        "value": [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "x", "y", "z"
        ]
    },
    "upperChar": {
        "type": "string",
        "value": [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "X", "Y", "Z"
        ]
    },
    "boolean": {
        "type": "bool",
        "value": [
            True, False
        ]
    },
    "int32": {
        "type": "int",
        "value": {
            "min": 0,
            "max": 2147483647
        }
    },
    "int64": {
        "type": "int",
        "value": {
            "min": 0,
            "max": 9223372036854775807
        }
    },
    "fullName": {
        "type": "string",
        "value": "||firstName|| ||lastName||"
    }
}

print("Creating structure...")

if does_file_exist(fileName):
    data = read_json_file(fileName)

    if "settings" not in data:
        data["settings"] = {}
    if "useDefaultValues" in data["settings"] and data["settings"]["useDefaultValues"] == False:
        pass
    else:
        data['library'] = {**data['library'], **deepcopy(defaultValues)}

    if "nullableChancePercentage" not in data["settings"]:
        data["settings"]["nullableChancePercentage"] = 10

    # print(data)
    for key in data['generate']:
        output[key['type']] = []
        for x in range(key['amount']):
            if key['type'] not in data['library']:
                print(f"Key {key['type']} not found in library")
                input("Press enter to exit...")
                exit()
            if data['library'][key['type']]['type'] == 'json':
                output[key['type']].append(deepcopy(data['library'][key['type']]['value']))
            else:
                output[key['type']].append("||" + key['type'] + "||")
            if 'nullable' in data['library'][key['type']]:
                for option in data['library'][key['type']]['nullable']:
                    if random.randint(0, 100) <= data['settings']['nullableChancePercentage']:
                        stringifiedOutput = stringify_json(output[key['type']][-1])
                        splitted = stringifiedOutput.split(f"\"{option}\":")
                        newValue = f"\"{option}\":null"
                        for i in range(len(splitted)):
                            # if it is not the first item, remove everything till the first comma
                            if i != 0:
                                splitted[i] = splitted[i].split('"', 2)[2]
                        stringifiedOutput = newValue.join(splitted)
                        output[key['type']][-1] = parse_json(stringifiedOutput)
                        
print("Replacing values...")
output = stringify_json(output)
while True:
    found = False
    for definedKeys in data['library'].keys():
        find = '||' + definedKeys + '||'
        if find in output:
            found = True
            selectedData = data['library'][definedKeys]
            output = getValue(selectedData, output)
            
    if not found:
        break

print("Converting to json file...")

write_json_file(exportFileName, parse_json(output))

print("Done!")
input("Press enter to exit...")