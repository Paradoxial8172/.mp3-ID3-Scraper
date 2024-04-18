from tinytag import TinyTag
import tkinter
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import io
import pygame
import os

def exit():
    root.destroy()

pygame.mixer.init()

root = tkinter.Tk()
root.geometry("500x500")

def open_file():
    file = fd.askopenfilename()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    return os.path.abspath(file)

def get_track_information(filename):

    filename = filename.replace("\\", "/")
    track = TinyTag.get(filename)
    album = track.album
    title = track.title
    artist = track.artist

    track_duration = track.duration
    hours = int(track_duration / 3600)
    minutes = int((track_duration - hours * 3600) / 60)
    seconds = int((track_duration - hours * 3600 - minutes * 60))
    readable_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    album_img_bytes_str = TinyTag.get(filename, image=True)

    if album_img_bytes_str.get_image() is None:
        image = ImageTk.PhotoImage(Image.open("no_album_cover.png"))
    else:
        img = Image.open(io.BytesIO(album_img_bytes_str.get_image())).resize((128,128))

        image = ImageTk.PhotoImage(img)

    info = {
        "Path": filename,
        "Title": title,
        "Artist": artist,
        "Album": album,
        "Duration": readable_duration,
        "Album_Img_Bytes": album_img_bytes_str.get_image()
    }

    lbl1.configure(text=f"Title: {info['Title']}")
    lbl2.configure(text=f"Artist: {info['Artist']}")
    lbl3.configure(text=f"Album: {info['Album']}")
    lbl4.configure(text=f"Duration: {info['Duration']}")
    lbl5.configure(text=f"Path: {info['Path']}")
    lbl6.configure(image=image)

    lbl6.image = image

image = ImageTk.PhotoImage(Image.open("no_album_cover.png"))

lbl1 = tkinter.Label(root, text=f"Title: {None}")
lbl2 = tkinter.Label(root, text=f"Artist: {None}")
lbl3 = tkinter.Label(root, text=f"Album: {None}")
lbl4 = tkinter.Label(root, text=f"Duration: {None}")
lbl5 = tkinter.Label(root, text=f"Path: {None}", wraplength=300)
lbl6 = tkinter.Label(root, image=image)

lbl6.image = image

b1 = tkinter.Button(root, text="Play", command=lambda: get_track_information(open_file()))

lbl1.pack()
lbl2.pack()
lbl3.pack()
lbl4.pack()
lbl5.pack()
lbl6.pack()

b1.pack()

root.protocol("WM_DELETE_WINDOW", exit)

root.mainloop()
