import os
import subprocess
# pip install yt-dlp

# Define the input file name
input_file = "message.txt"
output_file = "receipt.txt"
formatIndex = 0
formats = ["11", "18"]

# Ask the user to choose between MP3 and MP4
choice = input("Enter 'mp3' or 'mp4' to choose the download format: ")

if choice not in ["mp3", "mp4"]:
    print("Invalid choice. Please enter 'mp3' or 'mp4.")
else:

    while True:
        answer = input("Do you want to download from message.txt? Or by pasting the Url? (1/2):")
        if answer not in ["1", "2"]:
            print("Invalid choice. Please enter '1' or '2.")
        else:
            break




    output_folder = f"{choice}OutputFolder"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Change the working directory to the output folder
    os.chdir(output_folder)
    
    if answer == "1":
        # Open and read the lines from the input file
        with open(f"../{input_file}", "r") as file:
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

    # Loop through each line and run the appropriate yt-dlp command
    for line in lines:
        # Remove leading/trailing whitespace and newlines
        video_url = line.strip()
        if line == "\n" or line == "":
            continue
        # Remove the playlist part of the URL if it exists
        # https://www.youtube.com/watch?v=Ac_Y_LWvwNY&list=WL&index=5
        if "list=" in video_url:
            video_url = video_url.split("&list=")[0]
        # Construct the yt-dlp command based on the user's choice
        if choice == "mp4":
            while True:
                try:
                    command = ["yt-dlp", "-f", formats[formatIndex], video_url]
                    subprocess.run(command, check=True)
                    break
                except subprocess.CalledProcessError as e:
                    formatIndex += 1
                    print(f"Error downloading video from: {video_url}")
                    print(f"Error message: {e.stderr}")
                    if formatIndex >= len(formats):
                        print(f"Error downloading video from: {video_url}")
                        break
                    print(f"Trying to download with format: {formats[formatIndex]}")
                    continue
            formatIndex = 0
        else:
            command = ["yt-dlp", "-x", "--audio-format", "mp3", video_url]
        
            # Execute the command
            try:
                subprocess.run(command, check=True)
                print(f"Downloaded video from: {video_url} as {choice}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading video from: {video_url}")
                print(f"Error message: {e.stderr}")
    with open(f"../{output_file}", "w") as file:
        file.write("The Downloaded videos are:\n")
        for line in lines:
            file.write(line)
        file.write("\n")
        if choice == "mp3":
            file.write("Downloaded as mp3")
        else:
            file.write("Downloaded as mp4")

