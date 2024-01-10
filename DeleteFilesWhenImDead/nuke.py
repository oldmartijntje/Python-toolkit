import json
import os
import datetime
import logging
import time
import shutil

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

def int_to_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt

def has_passed_x_days(target_datetime, x):
    current_datetime = datetime.datetime.now()
    time_difference = current_datetime - target_datetime
    days_passed = time_difference.days
    return days_passed >= x

def delete_paths(paths):
    if "deletions" in get_value_from_json("SpecificLogging"):
        logIfAllowed(f"Going to delete", 'info')
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
            if "deletions" in get_value_from_json("SpecificLogging"):
                logIfAllowed(f"Deleted file: {path}", 'warning')
        elif os.path.isdir(path):
            shutil.rmtree(path)
            if "deletions" in get_value_from_json("SpecificLogging"):
                logIfAllowed(f"Deleted directory and its contents: {path}", 'warning')
        else:
            if "errors" in get_value_from_json("SpecificLogging"):
                logIfAllowed(f"Path not found: {path}", 'error')

def get_value_from_json(key, filename = 'settings.json'):
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
        logIfAllowed(f"Saved by turning on.", 'info')

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

def create_paths(paths):
    for path in paths:
        if path.endswith('/'):
            # If the path ends with '/', create a directory if it doesn't exist
            directory_path = path.rstrip('/')
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                if "create" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"Created directory: {directory_path}", 'info')
        else:
            # Otherwise, create a file if it doesn't exist
            if not os.path.exists(path):
                with open(path, 'w') as file:
                    file.write("")
                if "create" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"Created file: {path}", 'info')

def resetSettings():
    file_data = read_json_file(filename)
    for key in file_data:
        if key in get_value_from_json('ResetSettingsOnDeletion')['ResetTheFollowingSettingsOnDeletion']:
            try:
                if get_value_from_json('ResetSettingsOnDeletion')['CompareTo'] == "DEFAULT":
                    file_data[key] = defaultJson[key]
                else:
                    file_data[key] = get_value_from_json(key, get_value_from_json('ResetSettingsOnDeletion')['CompareTo'])
            except Exception as e:
                if "errors" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"{e}", 'error')
    write_json_file(filename, file_data)
    if "settings" in get_value_from_json("SpecificLogging"):
        logIfAllowed(f"Reset settings.", 'info')


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

if get_value_from_json("Nuke")["ActivateOtherJSON"] != "":
    filename = get_value_from_json("Nuke")["ActivateOtherJSON"]
    file_data = read_json_file(filename)
    if file_data:
        pass
    else:
        write_json_file(filename, defaultJson)
        file_data = defaultJson

if "nuke" in get_value_from_json("SpecificLogging"):
    logIfAllowed(f"Nuke initialized", 'warning')

try:
    if get_value_from_json("Nuke")["RequireConfirm"]:
        if get_value_from_json("Nuke")["RequirePassword"]:
            if input("CAUTION, Are you sure you want to nuke? (y/n): ") == "y":
                if "nuke" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"Entering password for nuke.", 'warning')
                while input("Enter password: ") != get_value_from_json("Nuke")["Password"]:
                    print("Incorrect password.")
                    if "nuke" in get_value_from_json("SpecificLogging"):
                        logIfAllowed(f"Incorrect password for nuke entered.", 'info')
            else:
                print("Cancelled.")
                if "nuke" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"Nuke cancelled", 'info')
                exit()
        else:
            if input("CAUTION, Are you sure you want to nuke? (y/n): ") == "y":
                pass
            else:
                print("Cancelled.")
                if "nuke" in get_value_from_json("SpecificLogging"):
                    logIfAllowed(f"Nuke cancelled", 'info')
                exit()
    elif get_value_from_json("Nuke")["RequirePassword"]:
        if "nuke" in get_value_from_json("SpecificLogging"):
            logIfAllowed(f"Entering password for nuke.", 'warning')
        while input("Enter password: ") != get_value_from_json("Nuke")["Password"]:
            print("Incorrect password.")
            if "nuke" in get_value_from_json("SpecificLogging"):
                logIfAllowed(f"Incorrect password for nuke entered.", 'info')

except Exception as e:
    if "errors" in get_value_from_json("SpecificLogging"):
        logIfAllowed(f"{e}", 'error')
    exit()

if "nuke" in get_value_from_json("SpecificLogging"):
    logIfAllowed(f"Nuke Activated", 'warning')

delete_paths(get_value_from_json('DeleteThesePaths'))
if get_value_from_json("SaveOnDeletion"):
    saveMeNow()
try:
    if get_value_from_json("ResetSettingsOnDeletion")["UseThisSetting"]:
        resetSettings()
except Exception as e:
    if "errors" in get_value_from_json("SpecificLogging"):
        logIfAllowed(f"{e}", 'error')
if get_value_from_json("AutoCreateOnDeletion"):
    create_paths(get_value_from_json("AutoCreateFolders"))
    create_paths(get_value_from_json("AutoCreateFiles"))