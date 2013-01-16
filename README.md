### Overview
I often use Chrome's bookmarking feature to store sites that I find interesting or enlightening, but I usually forget to dig through the folder I store the bookmarks in to look at them again.
To encourage myself to go back and visit these sites, I wrote this simple script that takes a set of names of Chrome bookmark folders and randomly chooses one of the bookmarks contained inside to open.
I've set the script to run on my startup, so now every time I log in Chrome loads up one of my favorite sites.

### Installation
You will need to define a JSON file listing the names of the Chrome bookmark folders you want to choose a bookmark from.
If you need help with the syntax, check out [the JSON site]("http://www.json.org/").
<i>Example:</i>
```json
[
    "FooFolder",
    "BarFolder",
    "ZapFolder"
]
```
<i>Folder names are capitalization-sensitive!</i>  

You will also need to tell the script where your JSON file is, so set the TARGET_FOLDERS_FILEPATH variable to the full path to the file, as in the code block below.
<i>Example</i>
```python
# Filepath to JSON file containing names of bookmark folders whose bookmarks will be used in random selection
TARGET_FOLDERS_FILEPATH = "~/.random-bookmark-folders.json"
```

The script will attempt to guess the path to your Chrome bookmark file, but you may need to manually specify it through the BOOKMARKS_FILEPATH variable as in the example below.
<i>Example</i>
```python
# Filepath to JSON file Chrome stores its Bookmarks in
BOOKMARKS_FILEPATH = "~/.config/google-chrome/Default/Bookmarks"
```
Now that everything's set up, you can open random bookmark by running the script!

### Troubleshooting
<b>Can't open the Chrome bookmark file</b>  
Try manually specifying the Chrome bookmark file path  
<br/>
<b>Can't open the JSON file of folder names</b>  
Double-check that the path you specified is correct   
<br/>
<b>No bookmark is opened when the script is run</b>  
Ensure that the names of the desired folders are properly spelled and the folders have bookmarks in them
