from collections import OrderedDict
from enum import Enum


class PassageType(Enum):
    TEXT = 0
    ENDPOINT = 1
    ROLL = 2
    TRIAL = 3
    END = 4
    FIGHT = 5
    ITEM_CHECK = 6
    EXEC = 7
    COUNTDOWN_START = 8
    COUNTDOWN_STOP = 9
    BACK = 10
    BACKTRACK = 11
    ITEM = 12
    TRIAL_COUNTDOWN_START = 13


class BodyType(Enum):
    TEXT = 0
    ROBOT = 1
    MIXED = 2


class BodyLineType(Enum):
    TEXT = 0
    POSE = 1
    SAY = 2
    FEEL = 3
    EMPTY = 4


class Passage:
    """
    A story passage parsed from an Harlowe Passage.

    Attributes:
    """

    def __init__(self, pid, name, contents, tags):
        self.pid = pid
        self.name = name
        self.contents = contents
        self.tags = tags

        self.passage_type = PassageType.TEXT

        self.trial_type = None
        self.trial_id = None
        self.trial_seq = None
        self.room_name = None
        self.is_trial = False

        self.destinations = {}
        self.parents = {}
        self.experiment_info = OrderedDict()
        self.init_methods = OrderedDict()
        self.body_lines = OrderedDict()
        self.links = OrderedDict()

        self.body_type = BodyType.TEXT
        self.line_to_body_type = {
            BodyLineType.TEXT: BodyType.TEXT,
            BodyLineType.POSE: BodyType.ROBOT,
            BodyLineType.SAY: BodyType.ROBOT,
            BodyLineType.FEEL: BodyType.ROBOT,
        }

    def set_trial(self, trial_type, trial_id, trial_seq):
        self.trial_type = trial_type
        self.trial_id = trial_id
        self.trial_seq = trial_seq
        self.is_trial = True

    def create_linked_body_lines(self):

        pointer = 0
        linked_lines = OrderedDict()
        keys = list(self.body_lines.keys())

        while pointer < len(keys):

            (blt, line) = self.body_lines[keys[pointer]]
            if blt == BodyLineType.TEXT and line.line == "":
                pointer += 1
                continue

            if (pointer + 1) < len(keys):
                (blt_next, nl) = self.body_lines[keys[pointer+1]]
                if blt_next == BodyLineType.TEXT and nl.line == "":
                    linked_lines[keys[pointer]] = (blt, line, BodyLineType.EMPTY)
                else:
                    linked_lines[keys[pointer]] = (blt, line, blt_next)
            else:
                linked_lines[keys[pointer]] = (blt, line, None)
            pointer += 1

        return linked_lines

    def create_body_chunks(self):

        parsed_body = OrderedDict()
        parsed_id = 0
        current_dict = OrderedDict()
        current_type = None

        for id, (blt, line) in self.body_lines.items():

            if self.line_to_body_type[blt] == BodyType.TEXT and line.line == "":
                continue

            if current_type is None:
                current_type = self.line_to_body_type[blt]

            if self.line_to_body_type[blt] == current_type:
                current_dict[id] = line

            else:
                if len(current_dict) == 0:
                    current_dict[id] = line
                else:
                    parsed_body[parsed_id] = (current_type, current_dict)
                    current_type = None
                    parsed_id += 1
                    current_dict = OrderedDict()
                    current_dict[id] = line

        if len(current_dict) != 0:
            parsed_body[parsed_id] = (current_type, current_dict)

        return parsed_body



    def update_stats(self):
        # For now it just sets the body type
        # In the future, who knows
        num_text = 0
        num_robot = 0
        for _, (lt, _) in self.body_lines.items():
            if lt in [BodyLineType.POSE, BodyLineType.FEEL, BodyLineType.SAY]:
                num_robot += 1
                if num_text > 0:
                    break
            else:
                num_text += 1
                if num_robot > 0:
                    break

        if num_text > 0:
            if num_robot > 0:
                self.body_type = BodyType.MIXED
            else:
                self.body_type = BodyType.TEXT
        else:
            self.body_type = BodyType.ROBOT

        pass

    def render(self, env):
        # Init
        for _, init_macro in self.init_methods.items():
            init_macro.exec(env)

        # Replace the variables if a line
        # Exec a command if countdown or robot exec
        # Render markdown
        for _, (_,  body) in self.body_lines.items():
            body.exec(env)

    def __str__(self):
        ret_str = ""
        for section in [self.init_methods.items(), self.body_lines.items(), self.links.items()]:
            for row, line in section:
                ret_str += str(row) + ":   " + str(line) + "\n"

        return ret_str

    def to_json(self):
        json_dict = {}
        json_dict['pid'] = self.pid
        json_dict['name'] = self.name
        json_dict['contents'] = self.contents
        json_dict['tags'] = self.tags
        json_dict['init_methods'] = {}
        json_dict['body_lines'] = {}
        json_dict['links'] = {}

        for name, method in self.init_methods.items():
            json_dict['init_methods'][name] = method.to_json()

        #for name, line in self.body_lines.items():
        #    json_dict['body_lines'][name] = line.to_json()

        for name, link in self.links.items():
            json_dict['links'][name] = link.to_json()

        return json_dict
