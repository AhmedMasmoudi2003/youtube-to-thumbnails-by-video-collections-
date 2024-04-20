import requests
from bs4 import BeautifulSoup
import os

def download_thumbnail(url, filename=None):
  """Downloads the thumbnail of a YouTube video from the provided URL using web scraping
  and saves it with a filename based on the URL (if not provided), adding a '.jpg' extension.

  Args:
      url (str): The URL of the YouTube video.
      filename (str, optional): The filename to save the downloaded thumbnail. Defaults to None.

  Returns:
      bool: True if download successful, False otherwise.
  """

  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example selector (adjust based on YouTube's HTML structure)
    thumbnail_element = soup.select_one('meta[property="og:image"]')

    if thumbnail_element:
      thumbnail_url = thumbnail_element['content']

      # Download the thumbnail using requests
      thumbnail_response = requests.get(thumbnail_url, stream=True)

      # Check for successful download status code
      if thumbnail_response.status_code == 200:
        # Create the directory if it doesn't exist
        os.makedirs('thumbnails', exist_ok=True)  # Create 'thumbnails' directory if needed

        # Extract the video ID or filename from the URL
        filename_parts = url.split("/")  # Split URL by '/'
        if filename is None:
          filename = filename_parts[-1]  # Use the last part (often video ID) as filename

        # Ensure filename has '.jpg' extension
        if not filename.endswith('.jpg'):
          filename += '.jpg'  # Add '.jpg' extension if missing

        # Save the downloaded thumbnail with the extracted filename
        with open(os.path.join('thumbnails', filename), 'wb') as f:
          for chunk in thumbnail_response.iter_content(1024):
            f.write(chunk)
        print(f"Downloaded thumbnail for: {url} saved as: thumbnails/{filename}")
        return True
      else:
        print(f"Error downloading thumbnail for {url}: Status code {thumbnail_response.status_code}")
        return False

    else:
      print(f"Thumbnail URL not found in the YouTube webpage for: {url}")
      return False

  except Exception as e:
    print(f"Error downloading thumbnail for {url}: {e}")
    return False

def download_thumbnails_from_file(filename):
  """Downloads thumbnails for YouTube video URLs listed in a text file,
  naming them based on the video links and adding '.jpg' extension.

  Args:
      filename (str): The path to the text file containing YouTube video URLs.
  """

  with open(filename, 'r') as f:
    for line in f:
      url = line.strip()  # Remove leading/trailing whitespace from URL
      if url:  # Check if line is not empty
        download_thumbnail(url)

# Example usage: Replace 'your_file.txt' with the actual filename
download_thumbnails_from_file('links.txt')
