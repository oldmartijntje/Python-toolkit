# Navigator

v1.4.0

- [Testdata Generator](#testdata-generator)
    - [Settings](#settings)
    - [Generate](#generate)
    - [Library](#library)
        - [Types](#types)
            - [String](#string)
            - [Bool](#bool)
            - [Intager](#int)
            - [JSON](#json)
            - [Float](#float)
            - [List](#list)
            - [Singularity](#singularity)
        - [Recursion (What are the "||" doing everywhere?)](#recursion)
        - [Warnings](#warnings)
        - [Advanced](#advanced)
    - [Seperate files](#seperate-files)
    - [Default Variables](#defaults)
- [Future](#future)

# Testdata Generator

- [Navigator](#navigator)

you have the input json: `input.json`. This json holds 3 items:
- `generate`
- `settings`
- `library`

I explain everything in more detail. My advise is to read in order. If you want to skip ahead, use the [Navigator](#navigator).

There also is an `template.json`, this exists as a place to start with importing your data.

## Settings

- [Navigator](#navigator)

the following snippet is what the json values are that work

```json
"settings": {
    "nullableChancePercentage": 10,
    "undefinedableChancePercentage": 10,
    "useDefaultValues": true,
    "returnIfSingularityIsEmpty": "||null||",
    "extraVariables": [],
    "useExtraVariables": false,
    "looping": 25,
},
```

- `nullableChancePercentage` is the % of how much it should make variables null. This only happens to variables that are set to be able to be null.
- `undefinedableChancePercentage` is the same as `nullableChancePercentage`, but then for the chance of deleting the variable.
- `useDefaultValues` decides if you make use of the default defined variables. More on that later.
- `returnIfSingularityIsEmpty` is the value that will be placed if a singularity turns empty. This value will be placed a s a string, that's why the default is `||null||`,
- `extraVariables` is a list of json files where you can keep extra variables stored. (so the input.json is less clutterish, and easier to edit.)
- `useExtraVariables` decides if you use `extraVariables`
- `looping` is the amount of times it checks for a variable per loop

You can delete them all. When they are deleted they will revert to the default values as shown above in the codebox.

## Generate

- [Navigator](#navigator)

First I'll show you an example:

```json
"generate": [
    {
        "type": "user",
        "amount": 10
    }
],
```

Generate is a list with dictionaries.
In these Dictionaries there are 2 values:
- `type` is the type of something you want to generate.
- `amount` is the amount of it you need. This needs to be an intager. Or a key to an singularity. 

```json
"generate": [
    {
        "type": "user",
        "amount": "randomiser"
    }
],
```

In the above example it will take the length of the [Singularity](#singularity) and create that many. 

Type needs to be defined in the `library`. Read [library](#library) for more information.

## Library

- [Navigator](#navigator)

I'll start with showing a codebox again:

```json
"user": {
    "type": "json",
    "value": {
        "name": "||firstName|| ||lastName||",
        "username": "||stringDigit||||upperChar||||boolean||||firstName||",
        "properties": {
            "isBald": "||boolean||"
        },
        "id": "||id||"
    },
    "nullable": [
        "username"
    ]
}
```

This is the default defined item in the `template.json`. It shows the feature this program is made for, generating test data.

This example is the `json` type, you have multiple types.

### Types

there are the following types:
- `json`
- `int`
- `bool`
- `string`
- `float`

every time has it's own things to know about it. I'll cover them 1 by 1.

### string

Let's start with the easiert, the string. I'll first show an example of the string type:

```json
"firstName": {
    "type": "string",
    "value": [
        "John", "Jane", "Jack", "Jill", "Jim", "Jenny", "Joe", "Jill", "Jesse", "Jasmine"
    ]
},
```

This is taken from the default variables. When the program sees it is a `string` type, it will grab one of the items from the list.

You can also make the value a string instead of a list:
```json
"fullName": {
    "type": "string",
    "value": "||firstName|| ||lastName||"
}
```



### bool

This is an example of a bool:

```json
"boolean": {
    "type": "bool",
    "value": [
        true, false
    ]
},
```

This is also taken from the default variables. WHen the program sees it is a `bool` type, it will grab a true or false. 

bool is also just a randomiser that removes quotes. so in theory you can also do the following:

```json
"null": {
    "type": "bool",
    "value": ["null"]
}
```

The above example will take the null string and place it as the null variable. Why does this work? I have no clue. But as long as this is mentioned here in the readme, it will still work. It's not adviced. I'd advice to use a [List](#list) instead. Just like I do it with the default variables.

### int

Again, here is an example:

```json
"int64": {
    "type": "int",
    "value": {
        "min": 0,
        "max": 9223372036854775807,
        "unique": false,
        "uniqueIdentifier": "id"
    }
},
```

This is again taken from the default variables. int will give you a random number.

- `min` is the minimum number.
- `max` is the maximum number.
- `unique`, if set to `true`, it will count from the `min` upwards, so that there won't be duplicates. It will ignore `max`
- `uniqueIdentifier` is the `unique` counter it uses, so if multiple things use `"henk"` then every generation will make it increment. even if used elsewhere. 

all the above arguments are optional, if they are missing they will default to:
```json
"min": 0,
"max": 100
"unique": false
```

with `unique` set to false, `uniqueIdentifier` will be ignored.

You can also turn `min` and `max` into numbers below 0, just remember that `min` should be smaller than `max`.

### json

already seen an example, but here is it again:

```json
"user": {
    "type": "json",
    "value": {
        "name": "||firstName|| ||lastName||",
        "username": "||stringDigit||||upperChar||||boolean||||firstName||",
        "properties": {
            "isBald": "||boolean||"
        },
        "id": "||id||"
    },
    "nullable": [
        "username"
    ],
    "undefinedable": [
        "properties.isBald"
    ]
}
```

The explenation for the [|| characters everywhere is here](#recursion).

- `nullable` makes it so that there is a chance to turn the variables in here into null, you can change the chance calculation in the [Settings](#settings). To make it work with nested values, you write the full path with <kbd>.</kbd> in between.
- `undefinedable` works the same as `nullable`. But instead ov setting the value to `null`, it deletes the value.

You can delete `nullable` and `undefinedable` if you don't need them.

If the path doesn't exist, it'll print it in the chat, and ignore it.

Anything in value can be your normal json. Make it however big you want, and in any way you want.

### float

Floats work the same as ints:

```json
"floats": {
    "type": "float",
    "value": {
        "min": 0.1,
        "max": 1000.0001,
        "unique": true,
        "uniqueIdentifier": "id"
    }
}
```

only differences between float and int:
- `unique` counts with steps of `0.1` if it's a float.

remember that if you use the same `uniqueIdentifier` between an int and float, it'll depend on which one gets checked first. The one that checks first gets to decide what variable it'll be.

### List

```json
"usernames": {
    "type": "list",
    "value": "||firstName||",
    "min": 1,
    "max": 10
}
```

the list has takes `value` and makes a list with `min`-`max` of the `value` in it. In this example i'd get a list of 1-10 names

- `min` is optional, defaults to 1
- `max` is optional, defaults to 10
- `value` is advised to be a string, but it can literally be everything, as shown in the next example:

```json
"usernames": {
    "type": "list",
    "value": [
        "||firstName||",
        null,
        "||firstName||.||lastName||",
        true,
        false,
        3.14,
        365,
        "henk",
        {
            "name": "||firstName|| ||lastName||"
        }
    ],
    "min": 1,
    "max": 10
}
```

This will work. But using the string method is the cleanest since then you'll keep the structure formatting the same across the document.

### Singularity

a singularity is a list of strings, these strings will be randomly grabbed from the list every time it is loaded, untill the list is empty.

```json
"randomizer": {
    "type": "singularity",
    "value": [
        "||firstName||",
        "||null||",
        "||fullName||",
        "||int64||",
        "||int32||",
        "||boolean||",
        "||upperChar||",
        "||lowerChar||",
        "||id||",
        "||stringDigit||",
        "||digit||",
        "||lastName||",
        "henk",
        "owo"
    ],
    "singularityId": "someRandomNumber",
    "redoIfSingularityIsEmpty": true
}
```

This is an example I used to test it.
- `value` should be a list of strings
- `singularityId` is where it saves the progress. If you have multiple singularities with the same id, it'll be the first one that defines it to add it's items to the list.
- `redoIfSingularityIsEmpty`, if it is `true`, it will refill the list if the list is empty, instead of using the default variable. 

### recursion

- [Navigator](#navigator)

As you can see, there are a lot of `||` everywhere:

```json
"user": {
    "type": "json",
    "value": {
        "name": "||firstName|| ||lastName||",
        "username": "||stringDigit||||upperChar||||boolean||||firstName||",
        "properties": {
            "isBald": "||boolean||"
        },
        "id": "||id||"
    },
    "nullable": [
        "username"
    ]
}
```

This is how the generator finds the veriables.

it knows to link `||firstName||` to:

```json
"firstName": {
    "type": "string",
    "value": [
        "John", "Jane", "Jack", "Jill", "Jim", "Jenny", "Joe", "Jill", "Jesse"
    ]
},
```

This works in recursion, if you change `firstName` into the following example:

```json
"firstName": {
    "type": "string",
    "value": [
        "||firstName||||firstName||", "Jane", "Jack", "Jill", "Jim"
    ]
},
```

Now there is a chance of a very long firstname being generated (In theory it is able to become endless.)

In the following example you can make a randomizer. Since `||word||` is able to turn into `first`, and then there will ben `||firstName||` as text, which will be changed. But it also has the cance to turn into `||secondName||` or `||secondName||` which are not defined in this example.
```json
"firstName": {
    "type": "string",
    "value": [
        "Jane", "Jack", "Jill", "Jim"
    ]
},
"randomNamePart": {
    "type": "string",
    "value": [
        "||||word||Name||"
    ]
},
"word": {
    "type": "string",
    "value": [
        "first", "second", "third"
    ]
},
```

### warnings

These following types:
- `bool`
- `json`
- `int`
- `float`

These will strip the quotes they touch from the json, because otherwise it'll still be seen as a string. This also means that if you want a number in your string that you will have to take a workaround (otherwise it'll crash).
This only applies to when your string will start or end with a randomised value of one of these types.

there are your 2 options of combining the above types with string (don't combine json with string, it'll crash anyway.)

- using extra quotes
- changing them into string.

### using extra quotes:

ONLY WORKS IF YOU DON'T USE THE NULLABLE ON THESE VARIABLES. [What is nullable?](#json)

```json
"isBald": "||boolean||a"
```

Turn the above json into the following:

```json
"isBald": "\"||boolean||\"a"
```

This will fix it. You need to place `\"` at both sides. 

### changing them into string

This is the better option since it's cleaner and works with nullable. [What is nullable?](#json)

```json
"boolean": {
    "type": "bool",
    "value": [
        true, false
    ]
},
```

You should turn the above example into the example below.

```json
"boolean": {
    "type": "string",
    "value": [
        true, false
    ]
},
```

Why this works get's explained [Here](#advanced).

### Advanced

```json
"boolean": {
    "type": "bool",
    "value": [
        true, false
    ]
},
```

You can change the above example into the example below and it will still work.

```json
"boolean": {
    "type": "string",
    "value": [
        true, false
    ]
},
```

The only thing this changes is that it will keep quotes <kbd>"</kbd> around the value.

This works with all types and they should still behave the same. Except for `float`, it won't work on that one. But it works on the other types.

Things that will start working differently:

- `unique` will add "1" to the end of the string instead of counting upwards.
- the `json` type will fully be stringified json.
- don't turn `min` or `max` into a string, If they stay as a int, it will work with the type being string. Otherwise it'll crash.

## seperate files

- [Navigator](#navigator)

you can create your own jsons with variables, to be able to sort them and make your input.json less cluttered. [Settings](#settings) has more info about this.

The only thing you have to do to make your file work is by making a .json file
and you can then do two things.

The clean approach:
```json
{
    "library": {
        "user2": {
            "type": "json",
            "value": {
                "name": "||firstName|| ||lastName||",
            }
        }
    }
}
```

or the lazy approach:
```json
{
    "user2": {
        "type": "json",
        "value": {
            "name": "||firstName|| ||lastName||"
        }
    }
}
```
Both works

## Defaults

- [Navigator](#navigator)

There are some default variables defined. You can use any of them by default, unless you overwrite them or turn them off in the settings. Here is that json:
```json
{
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
            "unique": true,
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
            true, false
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
        "value": null,
        "max": 1
    }
}
```

# Future

- [Navigator](#navigator)

Making the following types:
- datetime
- versioning