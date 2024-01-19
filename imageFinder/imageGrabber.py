from pytube import YouTube

def get_youtube_thumbnail(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Get the thumbnail URL
        thumbnail_url = yt.thumbnail_url
        
        # Print the thumbnail URL
        print("Thumbnail URL:", thumbnail_url)
        
        # You can download the thumbnail if needed
        # thumbnail_path = yt.thumbnail_url.split("?")[0]
        # yt.streams.filter(file_extension='jpg').first().download(output_path='.', filename='thumbnail.jpg')
        
    except Exception as e:
        print("Error:", str(e))

# Example usage
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
get_youtube_thumbnail(youtube_url)