import html5lib as html5lib
from bs4 import BeautifulSoup
from googletrans import Translator
from tqdm import tqdm

_STORY_TAG = 'tw-storydata'
_PASSAGE_TAG = 'tw-passagedata'

trans = Translator()

# Load the raw HTML from Twine
source = open("../../../Stories/smallest_sea.html", 'rt', encoding='utf8').read()
soup = BeautifulSoup(source, features="html.parser")
soup_passages = soup.find_all("tw-passagedata")

source = """
Ciao sono Dario
"""

res = trans.translate(source, src='it', dest="en").text


with tqdm(total=len(soup_passages)) as pbar:
    for sp in soup_passages:

        print("Source ---")
        print(sp.string)
        print("Trans ---")
        print(trans.translate(sp.string, dest='en').text)
        print("\n")

        sp.string.replace_with(trans.translate(sp.string).text)
        pbar.update(1)

print(soup)
with open("translated_sea.html", "w") as file:
    file.write(str(soup))