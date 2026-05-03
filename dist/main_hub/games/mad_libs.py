import random
import re
import json
import os

def load_stories(stories):
    #loads the story

    try:
        with open(stories, 'r') as f:
            data = json.load(f)
            return data["stories"]
    except FileNotFoundError:
        print(f"Error: {stories} not found!")
        return []
    
def run():
    
    stories = load_stories('stories.json')

    if not stories:
        return
    
    template = random.choice(stories)

    placeholders = re.findall(r"\[(.*?)]", template)

    print("--- External File Mad Libs ---")

    #loops through to get user input
    for p in placeholders:
    
     user_input = input(f"Enter a/an {p.replace('_', ' ')}: ")
     template = template.replace(f"[{p}]", user_input, 1)

    print("\n--- Your Final Story---")
    print(template)
