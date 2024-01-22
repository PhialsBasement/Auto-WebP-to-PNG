import os
import time
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

# Set the downloads folder based on the operating system
if platform.system() == "Windows":
    DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
elif platform.system() == "Linux":
    DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
else:
    raise Exception("Unsupported operating system")

API_ENDPOINT = "http://127.0.0.1:5000/convert"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == '.webp':
            # Retry up to 5 times with a 1-second delay
            for _ in range(5):
                if os.path.exists(file_path):
                    convert_and_replace(file_path)
                    break
                time.sleep(1)

def convert_and_replace(webp_path):
    with open(webp_path, 'rb') as webp_file:
        files = {'image': ('webp_image.webp', webp_file, 'image/webp')}
        response = requests.post(API_ENDPOINT, files=files)

        if response.status_code == 200:
            png_data = response.json().get('png_data', '')
            if png_data:
                png_path = webp_path.replace('.webp', '.png')
                with open(png_path, 'wb') as png_file:
                    png_file.write(png_data.encode('latin-1'))
                webp_file.close()
                os.remove(webp_path)
                print(f"File converted and replaced: {webp_path} -> {png_path}")
            else:
                print(f"Error converting file: {webp_path}, {response.json()}")
        else:
            print(f"Error communicating with the API: {response.status_code}, {response.text}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DOWNLOADS_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
