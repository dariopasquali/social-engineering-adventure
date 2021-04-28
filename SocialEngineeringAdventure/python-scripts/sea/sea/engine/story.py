from collections import OrderedDict

from sea.engine.harlowe_processor.harlowe import parse_harlowe_html
from sea.engine.harlowe_sea.PassageParser import *
from sea.engine.model.Passage import PassageType
from sea.engine.model.Room import *
from bs4 import BeautifulSoup
import json


class Story:
    def __init__(self):
        self.room_macros = {}
        self.init_macros = []

        # Full lists of story passages and links
        self.passages = {}
        self.links = {}

        # Passages and links divided among rooms with a predefined order
        self.rooms = {}
        self.order = []

    # Returns the ordered list of rooms
    def get_dungeon(self):
        dungeon = OrderedDict()

        for r in self.order:
            dungeon[r] = self.rooms[r]

        dungeon = OrderedDict(reversed(list(dungeon.items())))

        return dungeon

    # region PARSING_AND_CREATION

    # Set the order only if it contains only existing rooms
    def set_order(self, order):
        res = True
        for r in order:
            if (r not in self.rooms.keys()):
                res = False
                break

        if (res):
            self.order = order

        return res

    # Add a passage to the passage list
    def add_passage(self, name, passage):
        self.passages[name] = passage

    # Add a room macro to the story
    def add_empty_room(self, start_passage, room):
        self.room_macros[start_passage] = room

    def add_init_macro(self, macro):
        self.init_macros.append(macro)

    def get_init_macros(self):
        return self.init_macros

    # Recursively build the rooms traversing the story linked trees
    def __recursive_mark_room(self, passage, room):

        # If the passage is already marked just return
        if passage.room_name is not None:
            return

        # Mark the passage
        passage.room_name = room.name

        # Get the relative links and process them
        if passage.name in self.links.keys():
            links = self.links[passage.name]
            room.add_links(passage.name, links)

            # Trigger the Recursion
            for dest_p in links:
                self.__recursive_mark_room(self.passages[dest_p], room)

        # Otherwise the paragraph is an endpoint
        # So no recursion is needed

        # Finally add the passage to the room
        room.add_passage(passage)

        return

    # Navigate the passages links and build the linked trees
    # Then marks each node composing the rooms
    def build_linked_trees_and_rooms(self):

        # First build the linked trees
        for passage_name, passage in self.passages.items():
            for _, link in passage.links.items():
                to_p = link.toPassage

                if (to_p in self.passages):
                    passage.destinations[to_p] = self.passages[to_p]
                    self.passages[to_p].parents[passage_name] = passage

                    if (passage_name not in self.links):
                        self.links[passage_name] = []

                    self.links[passage_name].append(to_p)

        # Then navigate the linked trees and build the rooms
        for room_start, room_info in self.room_macros.items():

            # Create the room
            room = Room(room_info.name, room_info.start, room_info.right,
                        room_info.left, room_info.back, room_info.backtrack)
            # Get the start passage
            start_passage = self.passages[room_start]

            # Recursively populate the room
            self.__recursive_mark_room(start_passage, room)

            # If present, add a backtrack passage
            if room.backtrack_passage != "":
                passage = self.passages[room.backtrack_passage]
                passage.room_name = room.name
                room.add_passage(passage)

            # Store it
            self.rooms[room.name] = room

    # Class Method to parse a raw twine file
    @classmethod
    def parse_raw_twine_file(cls, raw_filename, store_json=False, json_name="story.json"):

        # Load the raw HTML from Twine
        source = open(raw_filename, 'rt', encoding='utf8').read()
        soup = BeautifulSoup(source, features="html.parser")

        # Extract just the story
        story_source = str(soup.find_all("tw-storydata")[0])

        # Extract each passage fro the html structure
        story_elems, other_elems, passages = parse_harlowe_html(story_source)
        parser = PassageParser()
        story = Story()

        # Build the story, parsing the passages and rooms
        for key, passage in passages.items():
            parsed_passage, room, _, _, configs = parser.parse(passage)
            if parsed_passage is not None:
                story.add_passage(parsed_passage.name, parsed_passage)

            if room is not None:
                story.add_empty_room(room.start, room)

            # Collect item, enemy and sound macros
            for macro in configs:
                story.add_init_macro(macro)

        # Bild the linked tree of passages
        story.build_linked_trees_and_rooms()

        if (store_json):
            with open(json_name, "w") as fn:
                json_story = json.dumps(story.to_json(), indent=4)
                fn.write(json_story)

        return story

    # endregion

    def get_passage(self, passage_name):
        return self.passages[passage_name]

    # region PRINTING
    def __str__(self):

        ret_str = "===== ROOMS ======="
        for _, room in self.rooms.items():
            ret_str += str(room) + "\n\n"

        return ret_str

    def to_json(self):

        json_dict = {'rooms': {}}
        for name, room in self.rooms.items():
            json_dict['rooms'][name] = room.to_json()

        return json_dict

    # endregion
