import json
import os
import datetime
import time
import shutil
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')
handler = logging.FileHandler('testTheSettings.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.warning("testing starts here:")

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

def int_to_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt

def has_passed_x_days(target_datetime, x):
    current_datetime = datetime.datetime.now()
    time_difference = current_datetime - target_datetime
    days_passed = time_difference.days
    return days_passed >= x

def delete_paths(paths):
    logger.info(f"is going to delete: {paths}")

def get_value_from_json(key, filename = 'settings.json'):
    file_data = read_json_file(filename)
    if key in file_data:
        return file_data[key]
    else:
        file_data[key] = defaultJson[key]
        write_json_file(filename, defaultJson)
        return defaultJson[key]

def saveMeNow():
    logger.info("is able to save")


def create_paths(paths, afterDeletion = False):
    for path in paths:
        if path.endswith('/'):
            if afterDeletion:
                logger.info(f"is going to create {path} as folder after deletion")
            else:
                logger.info(f"is going to create {path} as folder on startup")

        else:
            if afterDeletion:
                logger.info(f"is going to create {path} as file after deletion")
            else:
                logger.info(f"is going to create {path} as file on startup")


def resetSettings():
    file_data = read_json_file(filename)
    for key in file_data:
        if key in get_value_from_json('ResetSettingsOnDeletion')['ResetTheFollowingSettingsOnDeletion']:
            try:
                if get_value_from_json('ResetSettingsOnDeletion')['CompareTo'] == "DEFAULT":
                    temp = defaultJson[key]
                else:
                    temp = get_value_from_json(key, get_value_from_json('ResetSettingsOnDeletion')['CompareTo'])
                logger.info(f"Would reset '{key}' to '{temp}'")
            except Exception as e:
                logger.error(f"Error: {e}")
    write_json_file(filename, file_data)


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
    "SpecificLogging": ["create","errors", "settingsChange", "saves", "deletions", "nuke"],
    "Nuke": {
        "RequireConfirm": True,
        "RequirePassword": True,
        "Password": "404NF",
        "ActivateOtherJSON": ""
    }, 
    "SaveAnotherJSON": ""
}

originalFilename = input("give me the settings.json filepath (press enter if it's default):")
filename = originalFilename
if filename == "":
    filename = 'settings.json'

file_data = read_json_file(filename)
if file_data:
    pass
else:
    write_json_file(filename, defaultJson)
    file_data = defaultJson

if get_value_from_json('SaveOnStartup'):
    logger.info(f"Would save on startup")

delete_paths(get_value_from_json('DeleteThesePaths'))
if get_value_from_json("SaveOnDeletion"):
    logger.info(f"would save on deletion")
else:
    logger.info(f"would not save on deletion")
try:
    if get_value_from_json("ResetSettingsOnDeletion")["UseThisSetting"]:
        resetSettings()
    else:
        logger.info("Would not reset settings after deletion")
except Exception as e:
    logger.error(f"Error: {e}")
if get_value_from_json("AutoCreateOnDeletion"):
    create_paths(get_value_from_json("AutoCreateFolders"), True)
    create_paths(get_value_from_json("AutoCreateFiles"), True)
else:
    logger.info("Would not create anything after deletion")
if get_value_from_json("StopOnDeletion"):
    logger.info("Would stop on deletion")
else:
    logger.info(f"Would continue the loop after deletion")

create_paths(get_value_from_json("AutoCreateFolders"))
create_paths(get_value_from_json("AutoCreateFiles"))

logger.warning(f"The following tests are what would happen if you would run nuke.py with this.")

try:
    if get_value_from_json("Nuke")["ActivateOtherJSON"] != "":
        logger.info(f"there is another settings file it will nuke")
        filename = get_value_from_json("Nuke")["ActivateOtherJSON"]
        file_data = read_json_file(filename)
        if file_data:
            logger.info(f"it exists")
        else:
            write_json_file(filename, defaultJson)
            logger.info(f"it didn't exist yet, but now it is created")
            file_data = defaultJson

except Exception as e:
    logger.error(f"found an error {e}")


try:
    if get_value_from_json("Nuke")["RequireConfirm"]:
        if get_value_from_json("Nuke")["RequirePassword"]:
            logger.info(f"would ask for confirmation and password")
        else:
            logger.info(f"would ask for confirmation")
    elif get_value_from_json("Nuke")["RequirePassword"]:
        logger.info(f"would ask for password")

except Exception as e:
    logger.error(f"found an error {e}")

delete_paths(get_value_from_json('DeleteThesePaths'))
if get_value_from_json("SaveOnDeletion"):
    logger.info(f"would save on deletion")
else:
    logger.info(f"would not save on deletion")
try:
    if get_value_from_json("ResetSettingsOnDeletion")["UseThisSetting"]:
        resetSettings()
    else:
        logger.info("Would not reset settings after deletion")
except Exception as e:
    logger.error(f"Error: {e}")
if get_value_from_json("AutoCreateOnDeletion"):
    create_paths(get_value_from_json("AutoCreateFolders"), True)
    create_paths(get_value_from_json("AutoCreateFiles"), True)
else:
    logger.info("Would not create anything after deletion")

logger.warning(f"The following tests are what would happen if you would run keepItAlive.py with this.")

filename = originalFilename

file_data = read_json_file(filename)
if file_data:
    pass
else:
    write_json_file(filename, defaultJson)
    file_data = defaultJson

if get_value_from_json("SaveAnotherJSON") != "":
    logger.info(f"there is another settings file it will save")
    filename = get_value_from_json("SaveAnotherJSON")
    file_data = read_json_file(filename)
    if file_data:
        pass
    else:
        write_json_file(filename, defaultJson)
        logger.info(f"it didn't exist yet, but now it is created")
        file_data = defaultJson
    
saveMeNow()