from sea.engine.harlowe_sea.MacroParser import *
from sea.engine.model.Passage import Passage, PassageType, BodyLineType
from sea.engine.model.StoryLine import StoryLine


class PassageParser:

    def __init__(self):

        self.experiment = [
            'room',
            'endpoint',
            'trial',
            'backtrack',
        ]

        self.complex_commands = [
            'exec',
            'countdown'
        ]

        self.robot_control = [
            'pose',
            'say_feel',
            'say',
            'feel'
        ]

        self.configs = [
            'enemy',
            'item',
            'sound',
        ]
        self.methods = [
            'set',
            'add',
            'sub',
            'addItem',
            'addConsumable',
            'haveItem',
            'haveConsumable',
            'gain',
            'pay',
            'equip',
            'use',
            'useConsumable',
            'fight',
            'hit',
            'heal',
            'roll',
            'fail',
            'image',
            'playSound'
        ]
        self.links = ['link']
        # self.ifs = ['if']

        self.parsers_factory = MacroParserFactory()

        self.passage_type_mapping = {
            'endpoint': PassageType.ENDPOINT,
            'roll': PassageType.ROLL,
            'trial': PassageType.TRIAL,
            'end': PassageType.END,
            'fight': PassageType.FIGHT,
            'haveItem': PassageType.ITEM_CHECK,
            'haveConsumable': PassageType.ITEM_CHECK,
            'exec': PassageType.EXEC,
            'back': PassageType.BACK,
            'backtrack': PassageType.BACKTRACK,
            'countdown_start': PassageType.COUNTDOWN_START,
            'countdown_stop': PassageType.COUNTDOWN_STOP,
            'item': PassageType.ITEM,
            'trial_countdown_start': PassageType.TRIAL_COUNTDOWN_START
        }

        self.body_line_mapping = {
            "": BodyLineType.TEXT,
            "pose": BodyLineType.POSE,
            "feel": BodyLineType.FEEL,
            "say": BodyLineType.SAY,
            "say_feel": BodyLineType.SAY,
        }

    def parseKeywords(self, line, keywords):
        result = False
        parsed = None
        match_keyword = None

        for k in keywords:
            parser = self.parsers_factory.get_macro_parser(k)
            match = parser.check_and_parse(line)
            if match is not None:
                parsed = match
                result = True
                match_keyword = k
                break

        return result, parsed, match_keyword

    # Parse the content of the Story returning passages, rooms and trials
    def parse(self, passage):

        if passage.contents is None:
            return None

        content_lines = passage.contents.splitlines()
        row = 0
        myPassage = Passage(passage.pid, passage.name, passage.contents, passage.tags)

        room_macro = None
        trial_macro = None
        endpoint_macro = None

        config_macros = []

        link_id = 0

        for line in content_lines:
            result = False

            if line.strip() == "":
                row += 1
                continue

            if not result:
                result, parsed, keyword = self.parseKeywords(line, self.methods)
                if parsed is not None:
                    # print(result)
                    myPassage.init_methods[row] = parsed
                    if keyword in self.passage_type_mapping:
                        myPassage.passage_type = self.passage_type_mapping[keyword]

                    if myPassage.name == "VARIABLES":
                        config_macros.append(parsed)


            if not result:
                result, parsed, _ = self.parseKeywords(line, self.links)
                if parsed is not None:
                    # print(result)
                    myPassage.links[link_id] = parsed
                    link_id += 1

            if not result:
                result, parsed, keyword = self.parseKeywords(line, self.configs)
                if parsed is not None:
                    if keyword == 'item':
                        myPassage.passage_type = self.passage_type_mapping[keyword]
                        parsed.passage_name = myPassage.name

                    # Keep config macros separated
                    config_macros.append(parsed)

            if not result:
                result, parsed, keyword = self.parseKeywords(line, self.experiment)
                if parsed is not None:
                    # print(parsed)
                    myPassage.experiment_info[row] = parsed
                    if keyword in self.passage_type_mapping:
                        myPassage.passage_type = self.passage_type_mapping[keyword]

                    if keyword == 'room':
                        room_macro = parsed
                    elif keyword == 'trial':
                        trial_macro = parsed
                        myPassage.set_trial(parsed.risk_type, parsed.id, parsed.sequence)
                    elif keyword == 'endpoint':
                        endpoint_macro = parsed
                        if endpoint_macro.direction in ['end', 'back']:
                            myPassage.passage_type = self.passage_type_mapping[endpoint_macro.direction]

            if not result:
                result, parsed, keyword = self.parseKeywords(line, self.complex_commands)
                if parsed is not None:
                    # print(result)
                    myPassage.init_methods[row] = parsed

                    if keyword in self.passage_type_mapping:
                        myPassage.passage_type = self.passage_type_mapping[keyword]

                    if keyword == "countdown":
                        if trial_macro is not None:
                            myPassage.passage_type = self.passage_type_mapping["trial_countdown_start"]
                        else:
                            myPassage.passage_type = self.passage_type_mapping[keyword + "_" + parsed.event]

            if not result:
                result, parsed, keyword = self.parseKeywords(line, self.robot_control)
                if parsed is not None:
                    body_line = (self.body_line_mapping[keyword], parsed)
                    myPassage.body_lines[row] = body_line

            if not result:
                # print("Not Parsed     " + line)
                myPassage.body_lines[row] = (self.body_line_mapping[""], StoryLine(line))

            row += 1


        myPassage.update_stats() # For now it just sets the body type

        return myPassage, room_macro, endpoint_macro, trial_macro, config_macros
