#!/usr/bin/python

"""    IF YOU DO NOT FILL THESE VARS IN, THE SCRIPT WILL ATTEMPT TO GUESS THEM     """
""" ============================================================================== """
# Filepath to JSON file containing names of bookmark folders whose bookmarks will be used in random selection
TARGET_FOLDERS_FILEPATH = ""

# Filepath to JSON file Chrome stores its Bookmarks in
BOOKMARKS_FILEPATH = ""
""" ============================================================================== """

import webbrowser
import json
import os.path
from os import environ
import platform
from sys import exit
from random import sample

""" ==== HELPER FUNCTIONS ================================================================== """
"""
Given a list of items from the bookmark bar and a set of folder names to search for, add all URL
items under the target folders to the given set
 - items: list of items from bookmark bar
 - target_folders: set of names of folders to pull URLs from
 - target_urls: set to add folder URLs to
"""
def get_target_urls(items, target_folders, target_urls):
    for item in items:
        if "type" not in item or "name" not in item:
            raise KeyError("Item missing 'type' or 'name' field: " + str(item))
        if item["type"] == "folder":
            # If folder is one of the target folders, add the URLs under it to the target URL set
            if item["name"] in target_folders:
                get_folder_urls(item, target_urls)
            # If it isn't, search its children for target folders
            elif "children" in item:
                get_target_urls(item["children"], target_folders, target_urls)

"""
Given a pointer to a dict representing a bookmark folder, recursively add all URL items under 
the folder to the set of URLs being considered for random selection
- folder : dict representing a bookmark folder
- target_urls : set of URLs which bookmark will be chosen from
"""
def get_folder_urls(folder, target_urls):
    if "children" in folder:
        for item in folder["children"]:
            if item["type"] == "url":
                target_urls.add(item["url"])
            elif item["type"] == "folder":
                get_folder_urls(item, target_urls)



""" ====== MAIN CODE ================================================================ """
# Try to guess target folders filepath if not specified
system = platform.system()
windows_username = os.environ.get("USERNAME")
if TARGET_FOLDERS_FILEPATH == "" or TARGET_FOLDERS_FILEPATH == None:
    if system == "Linux":
        TARGET_FOLDERS_FILEPATH = "~/.random-bookmark-folders.json"
    elif system == "Windows":
        TARGET_FOLDERS_FILEPATH = "C:\\Users\\" + windows_username + "\\random-bookmark-folders.json"
    else:
        print("Unable to guess path to file specifying bookmark folders to use")
        exit()

# Try to guess filepath to Chrome bookmarks if none specified
if BOOKMARKS_FILEPATH == "" or BOOKMARKS_FILEPATH == None:
    if system == "Linux":
        BOOKMARKS_FILEPATH = "~/.config/google-chrome/Default/Bookmarks"
    elif system == "Windows":
        windows_username = os.environ.get("USERNAME")
        BOOKMARKS_FILEPATH  = "C:\\Users\\" + windows_username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
    else:
        print("Unable to guess Chrome bookmarks filepath; please specify manually")
        exit()

# Parse Chrome Bookmarks file into object
BOOKMARKS_FILEPATH = os.path.expanduser(BOOKMARKS_FILEPATH)
try:
    bookmarks_fp = open(BOOKMARKS_FILEPATH)
except IOError:
    print("Unable to open Chrome bookmark file; ensure that the filepath is correctly specified")
    exit()
bookmarks = json.load(bookmarks_fp)
bookmarks_bar = bookmarks["roots"]["bookmark_bar"]
bookmarks_fp.close()
# Exit if user's bookmark bar doesn't have bookmarks
if "children" not in bookmarks_bar:
    exit()

# Parse 'target folders' file into object
TARGET_FOLDERS_FILEPATH = os.path.expanduser(TARGET_FOLDERS_FILEPATH)
try:
    target_folders_fp = open(TARGET_FOLDERS_FILEPATH)
except IOError:
    print("Unable to open file specifying bookmark folders to use; ensure that the filepath is correctly specified")
    exit()
target_folders = json.load(target_folders_fp)
target_folders_fp.close()

# Generate set of URLs to select from
target_urls = set()
get_target_urls(bookmarks_bar["children"], target_folders, target_urls)
if len(target_urls) == 0:
    print ("No bookmarks to pull from; ensure your target folders are spelled correctly and they contain bookmarks")
    exit()

# Choose a random element from the target URL set and open in Chrome
selected_url = sample(target_urls, 1).pop()
webbrowser.open(selected_url)
