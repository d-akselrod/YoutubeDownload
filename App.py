import sys
import subprocess

try:
    import os
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from pytube import YouTube
    from moviepy.editor import *
except ImportError as e:
    missing_lib = str(e).split()[-1]  # Extract the missing library name from the error message
    choice = input(f"The '{missing_lib}' library is missing. Do you want to install it now? (y/n) ")
    if choice.lower() == "y":
        if sys.platform.startswith("win"):  # Windows
            subprocess.run(["pip", "install", missing_lib])
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["sudo", "apt-get", "install", f"python3-{missing_lib.lower()}"])
        else:
            print(f"Sorry, the '{missing_lib}' library cannot be installed automatically on your system.")
            print("Please install it manually and try again.")
            sys.exit(1)
    else:
        print("Please install the missing libraries and try again.")
        sys.exit(1)



def download_video():
    url = url_entry.get()
    file_type = file_type_var.get()
    folder_path = folder_var.get()
    filename = filename_var.get()

    if not url:
        messagebox.showerror("Error", "Enter the URL of the YouTube video")
        return

    if not folder_path:
        messagebox.showerror("Error", "Choose the destination folder")
        return

    try:
        yt = YouTube(url)
        if file_type == "mp4":
            video = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            video.download(folder_path, filename=filename)
        elif file_type == "mp3":
            video = yt.streams.filter(only_audio=True).first()
            output_path = video.download(folder_path)

            mp4_file = os.path.join(folder_path, video.default_filename)
            mp3_file = os.path.join(folder_path, f"{filename}.mp3")
            audio = AudioFileClip(mp4_file)
            audio.write_audiofile(mp3_file)
            audio.close()

            os.remove(mp4_file)

        messagebox.showinfo("Success", f"Download complete! Saved in '{folder_path}' as '{filename}.{file_type}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def browse_folder():
    folder_path = filedialog.askdirectory(title="Choose the destination folder")
    folder_var.set(folder_path)


root = tk.Tk()
root.title("YouTube Downloader")

# URL input
url_label = tk.Label(root, text="YouTube URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# File type selection
file_type_var = tk.StringVar()
file_type_var.set("mp4")
file_type_label = tk.Label(root, text="File type:")
file_type_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
mp4_radio = tk.Radiobutton(root, text="MP4", variable=file_type_var, value="mp4")
mp4_radio.grid(row=1, column=1, padx=5, pady=5, sticky="w")
mp3_radio = tk.Radiobutton(root, text="MP3", variable=file_type_var, value="mp3")
mp3_radio.grid(row=1, column=1, padx=60, pady=5, sticky="w")

# Folder selection
folder_var = tk.StringVar()
folder_label = tk.Label(root, text="Download location:")
folder_label.grid(row=2, column=0, padx=5, pady=5, sticky="e") 
folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.grid(row=2, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=2, column=2, padx=5, pady=5)

# Filename input
filename_var = tk.StringVar()
filename_label = tk.Label(root, text="File Name:")
filename_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

filename_entry = tk.Entry(root, textvariable=filename_var, width=50)
filename_entry.grid(row=3, column=1, padx=5, pady=5)

download_button = tk.Button(root, text="Download", command=download_video, width=15)
download_button.grid(row=4, column=1, padx=5, pady=15)

root.mainloop()