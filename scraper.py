from tinytag import TinyTag
import tkinter
from PIL import Image, ImageTk
import io

def exit():
    root.destroy()

def get_track_information(filename) -> dict:

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

    info = {
        "Title": title,
        "Artist": artist,
        "Album": album,
        "Duration": readable_duration
    }

    return info

user_input = input("Enter path of audio file:\n").strip('"')



root = tkinter.Tk()
root.geometry("500x500")

track_info = get_track_information(user_input)

album_img_bytes_str = TinyTag.get(user_input.replace("\\", "/"), image=True)

b = album_img_bytes_str.get_image()
try:
    image = Image.open(io.BytesIO(b))
    img = image.resize((128, 128))
    album_img = ImageTk.PhotoImage(img)
    
except:
    album_img = None

lbl1 = tkinter.Label(root, text=f"Title: {track_info['Title']}")
lbl2 = tkinter.Label(root, text=f"Artist/Band: {track_info['Artist']}")
lbl3 = tkinter.Label(root, text=f"Album: {track_info['Album']}")
lbl4 = tkinter.Label(root, text=f"Duration: {track_info['Duration']}")
lbl5 = tkinter.Label(root, text="Album Cover:")

if album_img is None:
    no_album_image = ImageTk.PhotoImage(Image.open("images/no_album_cover.png"))
    lbl6 = tkinter.Label(root, image=no_album_image)
else:
    lbl6 = tkinter.Label(root, image=album_img)

lbl1.pack()
lbl2.pack()
lbl3.pack()
lbl4.pack()
lbl5.pack()
lbl6.pack()

root.protocol("WM_DELETE_WINDOW", exit)

root.mainloop()
