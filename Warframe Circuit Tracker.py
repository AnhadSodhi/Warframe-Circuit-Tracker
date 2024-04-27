import requests
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import io

WarframesPerWeek = [
    ["Excalibur", "Trinity", "Ember"],
    ["Loki", "Mag", "Rhino"],
    ["Ash", "Frost", "Nyx"],
    ["Saryn", "Vauban", "Nova"],
    ["Nekros", "Valkyr", "Oberon"],
    ["Hydroid", "Mirage", "Limbo"],
    ["Mesa", "Chroma", "Atlas"],
    ["Ivara", "Inaros", "Titania"],
    ["Nidus", "Octavia", "Harrow"],
    ["Gara", "Khora", "Revenant"],
    ["Garuda", "Baruuk", "Hildryn"]
]

def getCurrentCircuitCode():
    allCode = requests.get("https://warframe.fandom.com/wiki/The_Circuit").content
    soup = BeautifulSoup(allCode, "html.parser")
    return soup.find_all("tr", bgcolor="#777")

def getCurrentWeek(circuitHTML):
    strong_tag = circuitHTML.find("strong")
    week = strong_tag.text.strip()
    return int(week[5])

def getCurrentWarframes(week):
    return WarframesPerWeek[week-1]

def getWarframePicture(warframeName):
    # Search for the image on Google and get the URL of the first result
    search_url = f"https://www.google.com/search?q={warframeName}+warframe&tbm=isch"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    img_url = img_tags[1]['src'] # Change index if necessary

    # Download the image and return it as a PIL Image object
    image_bytes = io.BytesIO(urllib.request.urlopen(img_url).read())
    img = Image.open(image_bytes)
    return img

def displayContent(week, warframes, warframePictures):
    root = tk.Tk()
    root.title("Warframe Circuit")

    # Display week
    week_label = tk.Label(root, text=f"Week {week}", font=("Helvetica", 16))
    week_label.pack()

    # Display warframes and their names
    for i, (warframe, picture) in enumerate(zip(warframes, warframePictures)):
        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, padx=10)

        img = ImageTk.PhotoImage(picture)
        picture_label = tk.Label(frame, image=img)
        picture_label.image = img
        picture_label.pack()

        name_label = tk.Label(frame, text=warframe, font=("Helvetica", 12))
        name_label.pack()

        # If three Warframes are displayed, move to the next row
        if (i + 1) % 3 == 0:
            tk.Frame(root, height=20).pack()  # Add some vertical space between rows

    root.mainloop()

def main():
    circuitHTML = getCurrentCircuitCode()
    week = getCurrentWeek(circuitHTML[0])
    warframes = getCurrentWarframes(week)
    warframePictures = [getWarframePicture(warframe) for warframe in warframes]

    displayContent(week, warframes, warframePictures)

if __name__ == "__main__":
    main()
