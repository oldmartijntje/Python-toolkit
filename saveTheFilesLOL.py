import json
import os
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')
handler = logging.FileHandler('my_log.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

def read_json_file(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    else:
        return False

def write_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def datetime_to_int(dt):
    timestamp = int(dt.timestamp())
    return timestamp

def get_value_from_json(key):
    file_data = read_json_file(filename)
    if key in file_data:
        return file_data[key]
    else:
        file_data[key] = defaultJson[key]
        write_json_file(filename, defaultJson)
        return defaultJson[key]

def saveMeNow():
    file_data = read_json_file(filename)
    file_data['LastTimeSaved'] = datetime_to_int(datetime.datetime.now())
    write_json_file(filename, file_data)
    if "saves" in get_value_from_json("SpecificLogging"):
        logIfAllowed(f"Saved by user.", 'info')

def logIfAllowed(message, mode):
    if get_value_from_json('Logging'):
        match mode:
            case 'info':
                logger.info(message)
            case 'debug':
                logger.debug(message)
            case 'warning':
                logger.warning(message)
            case 'error':
                logger.error(message)

defaultJson = {
    "DaysBetween": 14,
    "SleepMinutesWhileLoop": 60,
    "LastTimeSaved": 0,
    "SaveOnStartup":True,
    "DeleteThesePaths": ["deletableExample/", "deletableExample/deletableFile.txt"],
    "Logging": True,
    "AutoCreateFolders": ["deletableExample/"],
    "AutoCreateFiles": ["deletableExample/deletableFile.txt"],
    "StopOnDeletion": False,
    "SaveOnDeletion": True,
    "AutoCreateOnDeletion": True,
    "LoopAfterStartup": True,
    "ResetSettingsOnDeletion": {
        "ResetTheFollowingSettingsOnDeletion": ["AutoCreateFolders", "AutoCreateFiles", "DeleteThesePaths"],
        "UseThisSetting": False,
        "CompareTo": "DEFAULT"
    },
    "SpecificLogging": ["create","errors", "settings", "saves", "deletions", "nuke"],
    "Nuke": {
        "RequireConfirm": True,
        "RequirePassword": True,
        "Password": "404NF",
        "ActivateOtherJSON": ""
    }
}

filename = 'settings.json'

file_data = read_json_file(filename)
if file_data:
    pass
else:
    write_json_file(filename, defaultJson)
    file_data = defaultJson

saveMeNow()