# try:
import json
from pytube import YouTube
from pytube import Channel
import os
import requests
from bs4 import BeautifulSoup

def get_image_sources(html_string, settings={}, loop =0):
    image_sources = []
    if "typeToFind" not in settings:
        settings["typeToFind"] = "img"
    if "getType" not in settings:
        settings["getType"] = "src"
    if "imgIsChild" not in settings:
        settings["imgIsChild"] = False
    if "childSettings" not in settings:
        settings["childSettings"] = {}
    

    # Parse the HTML string using BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')

    # Find all image tags in the HTML
    img_tags = soup.find_all(settings["typeToFind"])

    # Extract source attribute from each image tag
    for img_tag in img_tags:
        if "required" in settings:
            for required in settings["required"]:
                if type(img_tag.get(required['where'])) != type(None):
                    val = img_tag.get(required['where'])
                    if val == required['equals'] or required['equals'] in val:
                        if settings["getType"] == "txt":
                            src = img_tag.get_text()
                            if src:
                                image_sources.append(src)
                            continue
                        if settings["imgIsChild"] and loop == 0:
                            src = get_image_sources(str(img_tag), settings["childSettings"], 1)
                            src = mergeSmolList(src)
                            if src:
                                image_sources.append(src)
                            continue
                        src = img_tag.get(settings["getType"])
                        if src:
                            image_sources.append(src)
        else:
            if settings["getType"] == "txt":
                src = img_tag.get_text()
                if src:
                    image_sources.append(src)
                continue
            if settings["imgIsChild"] and loop == 0:
                src = get_image_sources(str(img_tag), settings["childSettings"], 1)
                src = mergeSmolList(src)
                if src:
                    image_sources.append(src)
                continue
            src = img_tag.get(settings["getType"])
            if src:
                image_sources.append(src)

    return image_sources

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

def get_youtube_info(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Get the video title and thumbnail URL
        title = yt.title
        thumbnail_url = yt.thumbnail_url
        
        # Return a list containing title and thumbnail URL
        return [title, thumbnail_url]
        
        # You can download the thumbnail if needed
        # thumbnail_path = yt.thumbnail_url.split("?")[0]
        # yt.streams.filter(file_extension='jpg').first().download(output_path='.', filename='thumbnail.jpg')
        
    except Exception as e:
        print("Error:", str(e))
        return None
    
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def mergeSmolList(listt):
    if len(listt) == 0:
        listt = ""
    elif len(listt) == 1:
        listt = listt[0]
    return listt


# Define the input file name
input_file = "message.txt"
output_file = "receipt.txt"
formatIndex = 0
outputList = []
model = {
        "url": "",
        "image": "",
        "title": "",
        "description": "",
        "bannerText": ""
    }


while True:
    answer = input("Do you want to download from message.txt? Or by pasting the Url? (1/2):")
    if answer not in ["1", "2"]:
        print("Invalid choice. Please enter '1' or '2.")
    else:
        break

output_folder = f"OutputFolder"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

if answer == "1":
    # Open and read the lines from the input file
    with open(f"{input_file}", "r") as file:
        lines = file.readlines()
elif answer == "2":
    # Ask the user to paste the video URLs
    print("Enter the video URLs. Press enter after each URL. Press enter twice to start the download.")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

for line in lines:
    # Remove leading/trailing whitespace and newlines
    website_url = line.strip()
    if line == "\n" or line == "":
        continue

    if ("youtube" in website_url and "watch?v=" in website_url) or "youtu.be" in website_url:
        result = get_youtube_info(website_url)
        if result is not None:
            model["url"] = website_url
            model["image"] = result[1]
            model["title"] = result[0]
            model["description"] = ""
            model["bannerText"] = "Youtube Video"
            outputList.append(model)
            model = {
                "url": "",
                "image": "",
                "title": "",
                "description": "",
                "bannerText": ""
            }
            continue

    result = get_html(website_url)
    if result is not None:
        whatIsIt = "Website"
        title = "",
        images = ""
        if "store.steampowered.com/app" in website_url:
            whatIsIt = "Game"
            title = get_image_sources(result, {"required": [{"where": "id", "equals": "appHubAppName"}], "typeToFind": "div", "getType": "txt"})
            images = get_image_sources(result, {"required": [{"where": "class", "equals": ["game_header_image_full"]}]})
        elif "urbandictionary.com/define" in website_url:
            titleParts = website_url.split("?term=")
            title = titleParts[len(titleParts) - 1]
            title = title.replace("%20", " ")
            images = "https://i.imgur.com/DD7StZ3.png"
            whatIsIt = "Article"
        elif "modrinth" in website_url:
            title = get_image_sources(result, {"required": [{"where": "class", "equals": "title"}], "typeToFind": "h1", "getType": "txt"})
            images = get_image_sources(result, {"required": [{"where": "class", "equals": "project__icon"}], "typeToFind": "img", "getType": "src"}),
            whatIsIt = "Item"
        elif "roblox.com/catalog" in website_url:
            titleParts = website_url.split("/")
            title = titleParts[len(titleParts) - 1]
            title = title.replace("-", " ")
            whatIsIt = "Item"
        elif "roblox.com/games/" in website_url:
            titleParts = website_url.split("/")
            title = titleParts[len(titleParts) - 1]
            title = title.replace("-", " ")
            whatIsIt = "Game"
            # images = get_image_sources(result, {"required": [{"where": "class", "equals": "thumbnail-2d-container"}], "typeToFind": "span", "imgIsChild": True, "childSettings": {"typeToFind": "img", "getType": "src"}})
        elif "steamcommunity.com/" in website_url:
            title = get_image_sources(result, {"required": [{"where": "class", "equals": "workshopItemTitle"}], "typeToFind": "div", "getType": "txt"})
            images = get_image_sources(result, {"required": [{"where": "class", "equals": "guidePreviewImage"}], "typeToFind": "div", "getType": "img", "imgIsChild": True, "childSettings": {"typeToFind": "img", "getType": "src"}}),
            whatIsIt = "Item"
        
        elif website_url.endswith(".png") or website_url.endswith(".jpg") or website_url.endswith(".jpeg") or website_url.endswith(".gif"):
            images = [website_url]
        elif ".itch.io/" in website_url:
            title = website_url.split(".itch.io/")[1]
        else:
            images = get_image_sources(result)


        images = mergeSmolList(mergeSmolList(images))
        title = mergeSmolList(title)

        if type(images) == str and images.startswith("/"):
            images = website_url + images 

        model["url"] = website_url
        model["image"] = images
        model["title"] = title
        model["description"] = ""
        model["bannerText"] = whatIsIt
        outputList.append(model)
        model = {
            "url": "",
            "image": "",
            "title": "",
            "description": "",
            "bannerText": ""
        }
        continue
    else:
        print(f"Error downloading website: {website_url}")
        model["url"] = website_url
        outputList.append(model)
        model = {
            "url": "",
            "image": "",
            "title": "",
            "description": "",
            "bannerText": ""
        }

    

            

write_json_file(f"{output_folder}/output.json", outputList)


# except Exception as e:
#     print(f"Error: {e}")
#     input("Press enter to exit.")
#     exit()
