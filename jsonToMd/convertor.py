# for every file in /input, load it as a json object
import json
import os

try:
    os.listdir("input")
except FileNotFoundError:
    os.chdir("jsonToMd")

if not os.path.exists("output"):
    os.mkdir("output")

for file in os.listdir("input"):
    finalText=""
    number = 0
    if file.endswith(".json"):
        with open(f"input/{file}", "r", encoding="utf-8") as f:
            data = json.load(f, strict=False)
            data = data[::-1]
            # print(data)
            # for each key in the json object, create a new file in /output
            for key in data:
                number += 1
                # print(key)
                # check for key['link']
                if key.get('link') is None:
                    finalText+= f"- [ ] {number}.{key['title']}\n\n"
                else:
                    finalText+= f"- [ ] [{number}.{key['title']}]({key['link']})\n\n"
            with open(f"output/{file.split('.')[0]}.md", "w", encoding="utf-8") as f:
                f.write(finalText)