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

def getRandomFromData(data, fullJsonObject, officialData):
    if fullJsonObject['type'] == 'singularity':
        if fullJsonObject['singularityId'] not in usedSingularityIds:
            usedSingularityIds[fullJsonObject['singularityId']] = deepcopy(data)
        if len(usedSingularityIds[fullJsonObject['singularityId']]) == 0:
            if "redoIfSingularityIsEmpty" in fullJsonObject and fullJsonObject["redoIfSingularityIsEmpty"] == True:
                usedSingularityIds[fullJsonObject['singularityId']] = deepcopy(data)
            else:
                return officialData['settings']['returnIfSingularityIsEmpty']
        randomInt = random.randint(0, len(usedSingularityIds[fullJsonObject['singularityId']]) - 1)
        variable = usedSingularityIds[fullJsonObject['singularityId']][randomInt]
        usedSingularityIds[fullJsonObject['singularityId']].pop(randomInt)
        return variable
    elif fullJsonObject['type'] == 'list':
        if 'min' not in fullJsonObject:
            fullJsonObject['min'] = 1
        if 'max' not in fullJsonObject:
            fullJsonObject['max'] = 10
        var = [ data for x in range(random.randint(fullJsonObject['min'], fullJsonObject['max']))]
        return stringify_json(var)
    if type(data) is list:
        return data[random.randint(0, len(data) - 1)]
    elif type(data) is dict:
        if 'unique' in data and data['unique'] == True and 'uniqueIdentifier' in data:
            if data["uniqueIdentifier"] in usedVariableForIds:
                if type(usedVariableForIds[data["uniqueIdentifier"]]) is str:
                    usedVariableForIds[data["uniqueIdentifier"]] = usedVariableForIds[data["uniqueIdentifier"]] + "1"
                elif type(usedVariableForIds[data["uniqueIdentifier"]]) is float:
                    usedVariableForIds[data["uniqueIdentifier"]] = usedVariableForIds[data["uniqueIdentifier"]] + 0.1
                else:
                    usedVariableForIds[data["uniqueIdentifier"]] += 1
            else:
                if 'min' in data:
                    usedVariableForIds[data["uniqueIdentifier"]] = data['min']
                elif fullJsonObject['type'] == 'float':
                    usedVariableForIds[data["uniqueIdentifier"]] = 0.1
                else:
                    usedVariableForIds[data["uniqueIdentifier"]] = 0
            return usedVariableForIds[data["uniqueIdentifier"]]
        elif 'min' in data and 'max' in data:
            if fullJsonObject['type'] == 'float':
                return random.uniform(data['min'], data['max'])
            else:
                return random.randint(data['min'], data['max'])
        elif 'min' in data:
            if fullJsonObject['type'] == 'float':
                return random.uniform(data['min'], 100)
            else:
                return random.randint(data['min'], 100.001)
        elif 'max' in data:
            if fullJsonObject['type'] == 'float':
                return random.uniform(0, data['max'])
            else:
                return random.randint(0.1, data['max'])
        elif fullJsonObject['type'] == 'json':
            if 'test' in fullJsonObject:
                1 + 1
            newJson = deepcopy(fullJsonObject)
            newJson = checkForNullAndUndefined(newJson)
            return stringify_json(newJson)
        else:
            return data
    else:
        return data
    
def printError(error):
    if error not in errors:
        errors.append(error)
        print(error)
    
def getValue(selectedData, output, officialData):
    randomValue = getRandomFromData(selectedData['value'], selectedData, officialData)
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
        case 'list':
            output = checkForPureString(output, find, randomValue)
        case 'singularity':
            output = output.split(find, 1)[0] + str(randomValue) + output.split(find, 1)[1]
    return output

def edit_nested_value(data, path, new_value):
    keys = path.split('.')
    current = data
    try:
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = new_value
        return True
    except KeyError:
        return False

def delete_nested_value(data, path):
    keys = path.split('.')
    current = data
    try:
        for key in keys[:-1]:
            current = current[key]
        del current[keys[-1]]
        return True
    except (KeyError, TypeError):
        return False
    
def checkForNullAndUndefined(output):
    if 'nullable' in output:
        for option in output['nullable']:
            if random.randint(0, 100) <= data['settings']['nullableChancePercentage']:
                if not edit_nested_value(output['value'], option, None):
                    printError(f"Key {option} not found in variable, unable to set to null")
    if 'undefinedable' in output:
        for option in output['undefinedable']:
            if random.randint(0, 100) <= data['settings']['undefinedableChancePercentage']:
                if not delete_nested_value(output['value'], option):
                    printError(f"Key {option} not found in variable, unable to delete")
    return output['value']

output = {}
usedVariableForIds = {}
usedSingularityIds = {}
fileName = 'input.json'
exportFileName = 'output.json'
errors = []

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
    },
    "null": {
        "type": "list",
        "value": None,
        "max": 1
    }
}
loops = 0

version = "1.3.0"
print(f"Welcome to the json generator version {version} by OldMartijntje")
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

    if "undefinedableChancePercentage" not in data["settings"]:
        data["settings"]["undefinedableChancePercentage"] = 10

    if "returnIfSingularityIsEmpty" not in data["settings"]:
        data["settings"]["returnIfSingularityIsEmpty"] = "||null||"

    if "useExtraVariables" not in data["settings"] or data["settings"]["useExtraVariables"] == False:
        data["settings"]['extraVariables'] = []
    elif 'extraVariables' not in data["settings"]:
        data["settings"]['extraVariables'] = []
    
    if len(data["settings"]['extraVariables']) > 0:
        for extraVariable in data["settings"]['extraVariables']:
            if does_file_exist(extraVariable):
                extraData = read_json_file(extraVariable)
                if 'library' in extraData:
                    data['library'] = {**data['library'], **deepcopy(extraData['library'])}
                elif type(extraData) is dict:
                    data['library'] = {**data['library'], **deepcopy(extraData)}
                else:
                    print(f"Library not found in {extraVariable}")
            else:
                print(f"File {extraVariable} not found")
            

    # print(data)
    for key in data['generate']:
        output[key['type']] = []
        if 'amount' not in key:
            key['amount'] = 1
        if type(key['amount']) is str and key['amount'] in data['library'] and data['library'][key['amount']]['type'] == 'singularity':
            key['amount'] = len(data['library'][key['amount']]['value'])
        elif type(key['amount']) is not int: 
            print(f"Key {key['amount']} not found in library as a singularity, nor is it an integer")
            input("Press enter to exit...")
            exit()
        for x in range(key['amount']):
            if key['type'] not in data['library']:
                print(f"Key {key['type']} not found in library")
                input("Press enter to exit...")
                exit()
            if data['library'][key['type']]['type'] == 'json':
                output[key['type']].append(deepcopy(data['library'][key['type']]['value']))
                output[key['type']][-1] = checkForNullAndUndefined(deepcopy(data['library'][key['type']]))
            else:
                output[key['type']].append("||" + key['type'] + "||")
            
            

else:
    print("Input file not found")
    input("Press enter to exit...")
    exit()

print("Replacing values...")
output = stringify_json(output)
while True:
    found = False
    if loops % 100 == 0 and loops != 0:
        print(f"{loops} loops done, approx {output.count("|")// 4} values left to replace")
    for definedKeys in data['library'].keys():
        find = '||' + definedKeys + '||'
        if find in output:
            found = True
            selectedData = data['library'][definedKeys]
            output = getValue(selectedData, output, data)
    loops += 1    
    if not found:
        break

print("Converting to json file...")

write_json_file(exportFileName, parse_json(output))

print("Done!")
input("Press enter to exit...")