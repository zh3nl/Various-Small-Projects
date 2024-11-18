import json
import os
from datetime import datetime
from io import BytesIO
from typing import List

import pylast
import requests
from pick import pick
from PIL import Image, ImageDraw, ImageFont
from rich import print
from rich.panel import Panel
from rich.table import Table

LASTFM_API_KEY = "INSERT API KEY HERE"
LASTFM_API_SECRET = "INSERT API SECRET HERE"
network = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET)

# Save State in JSON
def load_or_create_json() -> None:
    if os.path.exists("albums.json"):
        with open("albums.json") as f:
            ratings = json.load(f)
    else:
        # Create a new json file with empty dict
        with open("albums.json", "w") as f:
            ratings = {"albums_ratings": [], "song_ratings": [], "tier_lists": []}
            json.dump(ratings, f)

# Get Album List
def get_album_list(artist: str) -> List[str]:
    # GET THE TOP ALBUMS OF THE ARTIST AND STORE THEM IN A LIST
    artist = network.get_artist(artist)
    top_albums = artist.get_top_albums()
    album_list = [str(album.item) for album in top_albums]

    # CLEANUP THE LIST
    for album in album_list:
        if "(null)" in album:
            album_list.remove(album)

    # SORT THE LIST
    album_list.sort()

    # ADD EXIT OPTION
    album_list.insert(0, "EXIT")
    return album_list

# Remove album from list
def create_tier_list_helper(albums_to_rank, tier_name):
    # If there are no more albums to rank, return an empty list
    if not albums_to_rank:
        return []

    question = f"Select the albums you want to rank in {tier_name}"
    tier_picks = pick(options=albums_to_rank, title=question, multiselect=True, indicator="→", min_selection_count=0)
    tier_picks = [x[0] for x in tier_picks]

    for album in tier_picks:
        albums_to_rank.remove(album)
    
    return tier_picks

# Return cover of selected albums
def get_album_cover(artist, album):
    album = network.get_album(artist, album)
    album_cover = album.get_cover_image()

    # Check if it's a valid URL
    try:
        response = requests.get(album_cover)
        if response.status_code != 200:
            album_cover = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    except:
        album_cover = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    
    return album_cover

# Create Tier List
def create_tier_list():
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)

    print("TIERS - S, A, B, C, D, E")

    question = "Which artist do you want to make a tier list for?"
    artist = input(question).strip().lower()

    try:
        get_artist = network.get_artist(artist)
        artist = get_artist.get_name()
        albums_to_rank = get_album_list(artist)

        # keep only the album name by splitting the string at the first - and removing the first element
        albums_to_rank = [x.split(" - ", 1)[1] for x in albums_to_rank[1:]]

        question = "What do you want to call this tier list?"
        tier_list_name = input(question).strip()

        # repeat until the user enters at least one character
        while not tier_list_name:
            print("Please enter at least one character")
            tier_list_name = input(question).strip()

        # S TIER
        question = "Select the albums you want to rank in S Tier:"
        s_tier_picks = create_tier_list_helper(albums_to_rank, "S Tier")
        s_tier_covers = [get_album_cover(artist, album) for album in s_tier_picks]
        s_tier = [{"album":album,"cover_art": cover} for album, cover in zip(s_tier_picks, s_tier_covers)]

        # A TIER
        question = "Select the albums you want to rank in A Tier:"
        a_tier_picks = create_tier_list_helper(albums_to_rank, "A Tier")
        a_tier_covers = [get_album_cover(artist, album) for album in a_tier_picks]
        a_tier = [{"album":album,"cover_art": cover} for album, cover in zip(a_tier_picks, a_tier_covers)]

        # B TIER
        question = "Select the albums you want to rank in B Tier:"
        b_tier_picks = create_tier_list_helper(albums_to_rank, "B Tier")
        b_tier_covers = [get_album_cover(artist, album) for album in b_tier_picks]
        b_tier = [{"album":album,"cover_art": cover} for album, cover in zip(b_tier_picks, b_tier_covers)]

        # C TIER
        question = "Select the albums you want to rank in C Tier:"
        c_tier_picks = create_tier_list_helper(albums_to_rank, "C Tier")
        c_tier_covers = [get_album_cover(artist, album) for album in c_tier_picks]
        c_tier = [{"album":album,"cover_art": cover} for album, cover in zip(c_tier_picks, c_tier_covers)]

        # D TIER
        question = "Select the albums you want to rank in D Tier:"
        d_tier_picks = create_tier_list_helper(albums_to_rank, "D Tier")
        d_tier_covers = [get_album_cover(artist, album) for album in d_tier_picks] 
        d_tier = [{"album":album,"cover_art": cover} for album, cover in zip(d_tier_picks, d_tier_covers)]
        # E TIER
        question = "Select the albums you want to rank in E Tier:"
        e_tier_picks = create_tier_list_helper(albums_to_rank, "E Tier")
        e_tier_covers = [get_album_cover(artist, album) for album in e_tier_picks]
        e_tier = [{"album":album,"cover_art": cover} for album, cover in zip(e_tier_picks, e_tier_covers)]

        # check if all tiers are empty and if so, exit
        if not any([s_tier_picks, a_tier_picks, b_tier_picks, c_tier_picks, d_tier_picks, e_tier_picks]):
            print("All tiers are empty. Exiting...")
            return


        # # add the albums that were picked to the tier list
        tier_list = {
            "tier_list_name": tier_list_name,
            "artist": artist,
            "s_tier": s_tier, 
            "a_tier": a_tier,
            "b_tier": b_tier,
            "c_tier": c_tier,
            "d_tier": d_tier,
            "e_tier": e_tier,
            "time": str(datetime.now())
        }

        # add the tier list to the json file
        album_file["tier_lists"].append(tier_list)

        # save the json file
        with open("albums.json", "w") as f:
            json.dump(album_file, f, indent=4)

        return

    except pylast.PyLastError:
        print("❌[b red] Artist not found [/b red]")

#Create Tier List Visualization
def image_generator(file_name, data):

    # return if the file already exists
    if os.path.exists(file_name):
        return

    # Set the image size and font
    image_width = 1920
    image_height = 5000
    font = ImageFont.truetype("arial.ttf", 15)
    tier_font = ImageFont.truetype("arial.ttf", 30)

    # Make a new image with the size and background color black
    image = Image.new("RGB", (image_width, image_height), "black")
    text_cutoff_value = 20

    #Initialize variables for row and column positions
    row_pos = 0
    col_pos = 0
    increment_size = 200

    """S Tier"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="red")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "S Tier", font=tier_font, fill="white")
        col_pos += increment_size

    for album in data["s_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))

        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))

        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))

        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0 

    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0

    """A TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="orange")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "A Tier", font=tier_font, fill="white")
        col_pos += increment_size

    for album in data["a_tier"]:
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0 

    row_pos += increment_size + 50
    col_pos = 0

    """B TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="yellow")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "B Tier", font=tier_font, fill="black")
        col_pos += increment_size

    for album in data["b_tier"]:
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0

    """C TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="green")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "C Tier", font=tier_font, fill="black")
        col_pos += increment_size

    for album in data["c_tier"]:
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))       
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0


    """D TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="blue")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "D Tier", font=tier_font, fill="black")
        col_pos += increment_size

    for album in data["d_tier"]:
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))        
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0


    """E TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="pink")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "E Tier", font=tier_font, fill="black")
        col_pos += increment_size

    for album in data["e_tier"]:

        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))    
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0

    image = image.crop((0, 0, image_width, row_pos))

    image.save(f"{file_name}")

# Export Created Image
def see_tier_lists():
    load_or_create_json()
    with open("albums.json", "r") as f:
        data = json.load(f)

    if not data["tier_lists"]:
        print("❌ [b red]No tier lists have been created yet![/b red]")
        return
    
    for key in data["tier_lists"]:
        image_generator(f"{key["tier_list_name"]}.png", key)
        print(f"✅ [b green]CREATED[/b green] {key['tier_list_name']} tier list.")

    print("✅ [b green]DONE[/b green]. Check the directory for the tier lists.")
    return
# Driver Code
def start():
    global network
    startup_question = "What do you want to do?"
    options = ["Rate by Album", "Rate Songs", "See Albums Rated", "See Songs Rated", "Make a Tier List", "See Created Tier Lists", "EXIT"]
    selected_options, index = pick(options, startup_question, indicator="→")

    if index == 0:
        rate_by_album()
    elif index == 1:
        rate_by_song()
    elif index == 2:
        see_albums_rated()
    elif index == 3:
        see_songs_rated()
    elif index == 4:
        create_tier_list()
    elif index == 5:
        see_tier_lists()
    elif index == 6:
        exit()

start()
