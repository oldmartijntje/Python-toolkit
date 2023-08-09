# Python-toolkit
some nice tools


## areYouDeadAlready.py + saveTheFilesLOL.py

These are two scripts that go together.

You can use this to secure private information. Everything stays safe, until you haven't confirmed that you are alive in X days. (highly customisable) If you haven't confirmed it for the set amount of days, it will delete the by you registered folders and files.

saveTheFilesLOL.py is the file you can manually confirm that you are alive.

areYouDeadAlready.py is the brains behind it, you should run this at startup.

It's customisable with the settings.json that it will autocreate on startup of either of the programs. It will have the following contents by default:

```JSON
{
    "DaysBetween": 14,
    "SleepMinutesWhileLoop": 60,
    "LastTimeSaved": 0,
    "SaveOnStartup": true,
    "DeleteThesePaths": [
        "deletableExample/",
        "deletableExample/deletableFile.txt"
    ],
    "Logging": true,
    "AutoCreateFolders": [
        "deletableExample/"
    ],
    "AutoCreateFiles": [
        "deletableExample/deletableFile.txt"
    ],
    "StopOnDeletion": false,
    "SaveOnDeletion": true,
    "AutoCreateOnDeletion": true,
    "LoopAfterStartup": true,
    "ResetSettingsOnDeletion": {
        "ResetTheFollowingSettingsOnDeletion": [
            "AutoCreateFolders",
            "AutoCreateFiles",
            "DeleteThesePaths"
        ],
        "UseThisSetting": true,
        "CompareTo": "DEFAULT"
    }
}
```
I will explain how everything works.

- `DaysBetween` is basically the name, how many days will it be before it deletes the stuff
- `SleepMinutesWhileLoop` is how many minutes it will take before it checks if the X days have passed again
- `LastTimeSaved` is the datetime moment of the last time you saved, this is used to calculate if it should delete, reccomended to just not touch it. (set it to 0 to make sure it will delete everything.)
- `SaveOnStartup` this will save every time you startup your pc automatically (checks beforehand if it has been X days, and will delete). this will make it so that you don't need to confirm your existance manually. This is able to work because I assume that if you are dead you wont restart your pc every day.
- `DeleteThesePaths` does what it says, put your file paths or directory paths here that you want to delete. NOTE: if you have C:/test as a file without file extention and a folder, and you put `"C:/test"` in `DeleteThesePaths`, it will delete both, cause it doesn't check for a `/` at the end of a string to make sure it's a folder
- `Logging` logs the deleted / created files. For debug purposes. And it's default on to make sure you know what files you lost / have randomly appeared. But yes I know you will probably turn it off.
- `AutoCreateFolders` will automatically create these folders if it doesn't exist.
- `AutoCreateFiles` will automatically create these files if it doesn't exist.
- `StopOnDeletion` will stop the program (areYouDeadAlready.py) after it has deleted once.
- `SaveOnDeletion` will set the `LastTimeSaved` to the current datetime after it has deleted your files
- `AutoCreateOnDeletion` does recreate the things you put in `AutoCreateFolders` and `AutoCreateFiles` after the deletion happens
- `LoopAfterStartup` makes it so it loops after checking once. if you turn this to false it will close the program (areYouDeadAlready.py) after checking once to see if it has been X days. which is instantly.
- `ResetSettingsOnDeletion` makes it so you can reset this settings.json when the files get deleted.
    - `ResetTheFollowingSettingsOnDeletion` will decide what settings will be reset. You can't reset only a single one of the `ResetSettingsOnDeletion` dictionary to reset, to reset any of these, reset `ResetSettingsOnDeletion`.
    - `UseThisSetting` will decide if you use this setting or not
    - `CompareTo` will decide on where it get's the settings it will reset from, if set to `DEFAULT` it will take the settings shown above, if set to another .json file, it will take the settings from there. Make sure it has the settings in there, and the file exists, this part does not have error handling / prevention. Probably handy to just copy paste the one auto-generated and put it to `settings copy.json`
