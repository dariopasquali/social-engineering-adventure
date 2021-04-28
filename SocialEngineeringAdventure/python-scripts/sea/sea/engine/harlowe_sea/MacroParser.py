import re
from sea.engine.model.Macros import *



class MacroParserFactory:

    def __init__(self):
        _MACRO_PATTERN_NAME_VAR_ELEMENT = r"""(\({0}: \$(?P<leftVar>[\w]*), (?P<rightVal>[\w\d\s\D]*)\)|\({0}: \$(?P<leftVar2>[\w]*), \$(?P<rightVar>[\w\d\s\D]*)\))"""
        _MACRO_PATTERN_NAME_ELEMENT_VAR = r"""\({0}: (?P<name>[\w\d\s\D]*), (?P<checkResult>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_NAME_VAL = r"""\({0}: (?P<value>[\w\d\s\D]*)\)"""
        _MACRO_ADD_CONSUMABLE = r"""\(addConsumable: (?P<name>[\w\d\s\D\w]*), (?P<qta>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_ROLL = r"""\(roll: (?P<cd>[\w]*)\)"""

        _MACRO_PATTERN_ENEMY = r"""\(enemy: (?P<name>[\w\d\s\D]*), (?P<def>[\w]*), (?P<dmg>[\w]*)\)"""
        _MACRO_PATTERN_ITEM = r"""\(item: (?P<name>[\w\d\s\D]*), (?P<type>[\w\d\s\D]*), (?P<value>[\w]*), (?P<effect>[\w\d\s\D]*)\)"""

        _MACRO_PATTERN_ADD_ITEM = r"""\(addItem: (?P<name>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_IMAGE = r"""\(image: (?P<name>[\w\d\s\D]*)\)"""

        _MACRO_PATTERN_ROOM = r"""\(room: (?P<name>[\w\d\s\D]*), (?P<start>[\w\d\s\D]*), (?P<right>[\w\d\s\D]*), (?P<left>[\w\d\s\D]*), (?P<back>[\w\d\s\D]*), (?P<backtrack>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_ENDPOINT = r"""\(endpoint: (?P<room>[\w\d\s\D]*), (?P<direction>"right"|"left"|"back"|"end")\)"""
        _MACRO_PATTERN_TRIAL = r"""\(trial: (?P<risk_type>"R"|"SE"|"SER"), (?P<id>[\w\d\s\D]*), (?P<sequence>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_BACKTRACK = r"""\(backtrack: (?P<room>[\w\d\s\D]*)\)"""

        _MACRO_PATTERN_COUNTDOWN = r"""\(countdown: (?P<seconds>[\w]*), (?P<event>[\w\d\s\D]*), (?P<timeout_passage>[\w\d\s\D]*)\)"""
        _MACRO_PATTERN_EXEC = r"""\(exec: (?P<command>[\w\d\s\D]*)\)"""

        _LINK_PATTERN = r""">>\[\[(?P<from>[\w\d\s\D]*)\|(?P<to>[\w ]*)\]\]"""
        _IF_PATTERN = r"""\(if: \$(?P<checkVar>[\w]*) is (?P<value>[\w]*)\)\[(?P<text>[\w\d\s\D]*)\]"""

        __HAVE_ITEM_MACRO = r"""\(haveItem: (?P<name>[\w\d\s\D]*), (?P<linkID>[\w\d\s\D]*)\)"""

        __MACRO_SOUND_PLAY = r"""\(playSound: (?P<event>[\w\d\s\D]*), (?P<mode>"background"|"once")\)"""
        __MACRO_SOUND_CREATE = r"""\(sound: (?P<event>[\w\d\s\D]*), (?P<name>[\w\d\s\D]*)\)"""

        __MACRO_POSE = r"""\(pose: (?P<name>[\w\d\s\D]*)\)"""
        __MACRO_SAY = r"""\(say: (?P<sentence>[\w\d\s\D]*)\)"""
        __MACRO_SAY_FEEL = r"""\(say: (?P<sentence>["][\w\d\s\D]*["]), (?P<emotion>[\w\d\s\D]*)\)"""
        __MACRO_FEEL = r"""\(feel: (?P<emotion>[\w\d\s\D]*)\)"""
        __MACRO_FAIL = r"""\(fail:\)"""

        self.regexes = {
            'set': _MACRO_PATTERN_NAME_VAR_ELEMENT.format('set'),
            'add': _MACRO_PATTERN_NAME_VAR_ELEMENT.format('add'),
            'sub': _MACRO_PATTERN_NAME_VAR_ELEMENT.format('sub'),
            'addItem': _MACRO_PATTERN_ADD_ITEM,
            'addConsumable': _MACRO_ADD_CONSUMABLE,
            'haveItem': __HAVE_ITEM_MACRO,
            'haveConsumable': _MACRO_PATTERN_NAME_ELEMENT_VAR.format('haveConsumable'),
            'gain': _MACRO_PATTERN_NAME_VAL.format('gain'),
            'pay': _MACRO_PATTERN_NAME_VAL.format('pay'),
            'equip': _MACRO_PATTERN_NAME_VAL.format('equip'),
            'use': _MACRO_PATTERN_NAME_VAL.format('use'),
            'useConsumable': _MACRO_PATTERN_NAME_VAL.format('useConsumable'),
            'fight': _MACRO_PATTERN_NAME_VAL.format('fight'),
            'hit': _MACRO_PATTERN_NAME_VAL.format('hit'),
            'heal': _MACRO_PATTERN_NAME_VAL.format('heal'),
            'roll': _MACRO_PATTERN_ROLL,
            'enemy': _MACRO_PATTERN_ENEMY,
            'item': _MACRO_PATTERN_ITEM,
            'link': _LINK_PATTERN,
            #'if': _IF_PATTERN,
            'room': _MACRO_PATTERN_ROOM,
            'endpoint': _MACRO_PATTERN_ENDPOINT,
            'trial': _MACRO_PATTERN_TRIAL,
            'backtrack': _MACRO_PATTERN_BACKTRACK,
            'image': _MACRO_PATTERN_IMAGE,
            'countdown': _MACRO_PATTERN_COUNTDOWN,
            'exec': _MACRO_PATTERN_EXEC,
            'playSound': __MACRO_SOUND_PLAY,
            'sound': __MACRO_SOUND_CREATE,

            'pose': __MACRO_POSE,
            'say': __MACRO_SAY,
            'say_feel': __MACRO_SAY_FEEL,
            'feel': __MACRO_FEEL,

            'fail': __MACRO_FAIL
        }

        self.parsers = {
            'set': SetMacroParser,
            'add': AddMacroParser,
            'sub': SubMacroParser,
            'haveConsumable': HaveConsumableMacroParser,
            'addConsumable': AddConsumableMacroParser,
            'haveItem': HaveItemMacroParser,
            'addItem': AddItemMacroParser,
            'gain': GainMacroParser,
            'pay': PayMacroParser,
            'equip': EquipMacroParser,
            'use': UseMacroParser,
            'useConsumable': UseConsumableMacroParser,
            'fight': FightMacroParser,
            'heal': HealMacroParser,
            'hit': HitMacroParser,
            'roll': RollMacroParser,
            'enemy': CreateEnemyMacroParser,
            'item': CreateItemMacroParser,

            'fail': FailMacroParser,


            'room' : RoomMacroParser,
            'endpoint' : EndpointMacroParser,
            'trial': TrialMacroParser,
            'backtrack': BacktrackMacroParser,
            'image': ImageMacroParser,
            'playSound': PlaySoundMacroParser,
            'sound': CreateSoundMacroParser,

            'countdown': CountdownMacroParser,
            'exec': ExecMacroParser,

            'pose': PoseParser,
            'say': SayParser,
            'say_feel': SayParser,
            'feel': FeelParser,

            'link': LinkMacroParser,
            #'if': IfMacroParser
        }

        # Init Parsers
        for key, value in self.regexes.items():
            self.parsers[key] = self.parsers[key](value)

    def get_macro_parser(self, keyword):
        return self.parsers[keyword]


class MacroParser:
    def __init__(self, regex):
        self.regex = regex
        self.compiled = re.compile(self.regex)
        self.incipt = None

        self.macro_factory = MacroFactory()

    def check_and_parse(self, text):
        if self.match_incipit(text):

            try:
                return self.parse(text)
            except AttributeError:
                print("FATAL PARSING ================= Check the regex! for {}".format(text))
                return None
        else:
            return None

    def parse(self, text):
        pass

    def match_incipit(self, text):
        return self.incipt in text


class SetMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(set:"

    def parse(self, text):
        match = self.compiled.match(text)

        leftVar = match.group('leftVar')
        rightVal = match.group('rightVal')
        rightVar = match.group('rightVar')

        macro = None

        if(rightVal is not None):
            macro = self.macro_factory.get_macro('set')(leftVar, rightVal)

        if(rightVar is not None):
            macro = self.macro_factory.get_macro('setVarVar')(leftVar, rightVar)

        return macro


class AddMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(add:"

    def parse(self, text):
        match = self.compiled.match(text)

        leftVar = match.group('leftVar')
        rightVal = match.group('rightVal')
        rightVar = match.group('rightVar')

        macro = None

        if(rightVal is not None):
            macro = self.macro_factory.get_macro('add')(leftVar, rightVal)

        if(rightVar is not None):
            macro = self.macro_factory.get_macro('addVarVar')(leftVar, rightVar)

        return macro


class SubMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(sub:"

    def parse(self, text):
        match = self.compiled.match(text)

        leftVar = match.group('leftVar')
        rightVal = match.group('rightVal')
        rightVar = match.group('rightVar')

        macro = None

        if(rightVal is not None):
            macro = self.macro_factory.get_macro('sub')(leftVar, rightVal)

        if(rightVar is not None):
            macro = self.macro_factory.get_macro('subVarVar')(leftVar, rightVar)

        return macro


class HaveConsumableMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(haveConsumable:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        resultVar = match.group('resultVar')

        macro = self.macro_factory.get_macro('haveConsumable')(name, resultVar)

        return macro


class AddConsumableMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(addConsumable:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        qta = match.group('qta')

        macro = self.macro_factory.get_macro('addConsumable')(name, qta)

        return macro


class HaveItemMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(haveItem:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        linkID = int(match.group('linkID'))

        macro = self.macro_factory.get_macro('haveItem')(name, linkID)

        return macro


class AddItemMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(addItem:"

    def parse(self, text):
        match = self.compiled.match(text)
        name = match.group('name').replace('\"', '')
        macro = self.macro_factory.get_macro('addItem')(name)

        return macro


class GainMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(gain:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value')
        macro = self.macro_factory.get_macro('gain')(value)

        return macro


class PayMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(pay:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value')
        macro = self.macro_factory.get_macro('pay')(value)

        return macro


class EquipMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(equip:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value').replace('\"', '')
        macro = self.macro_factory.get_macro('equip')(value)

        return macro


class UseMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(use:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value').replace('\"', '')
        macro = self.macro_factory.get_macro('use')(value)

        return macro


class UseConsumableMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(useConsumable:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value').replace('\"', '')
        macro = self.macro_factory.get_macro('useConsumable')(value)

        return macro


class FightMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(fight:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value').replace('\"', '')
        macro = self.macro_factory.get_macro('fight')(value)

        return macro


class HealMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(heal:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value')
        macro = self.macro_factory.get_macro('heal')(value)

        return macro


class HitMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(hit:"

    def parse(self, text):
        match = self.compiled.match(text)
        value = match.group('value')
        macro = self.macro_factory.get_macro('hit')(value)

        return macro


class RollMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(roll:"

    def parse(self, text):
        match = self.compiled.match(text)

        cd = match.group('cd')

        macro = self.macro_factory.get_macro('roll')(cd)

        return macro


class FailMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(fail:"

    def parse(self, text):
        macro = self.macro_factory.get_macro('fail')()
        return macro


class CreateEnemyMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(enemy:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        defense = int(match.group('def'))
        dmg = int(match.group('dmg'))

        macro = self.macro_factory.get_macro('enemy')(name, defense, dmg)

        return macro


class CreateItemMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(item:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        type = match.group('type').replace('\"', '')
        effect = match.group('effect').replace('\"', '')
        value = int(match.group('value'))

        macro = self.macro_factory.get_macro('item')(name, type, effect, value)

        return macro


class LinkMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = ">>[["

    def parse(self, text):
        match = self.compiled.match(text)

        fromPassage = match.group('from')
        toPassage = match.group('to')

        macro = self.macro_factory.get_macro('link')(fromPassage, toPassage)

        return macro


class RoomMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(room:"

    def parse(self, text):
        match = self.compiled.match(text)

        name = match.group('name').replace('\"', '')
        start = match.group('start').replace('\"', '')
        right = match.group('right').replace('\"', '')
        left = match.group('left').replace('\"', '')
        back = match.group('back').replace('\"', '')
        backtrack = match.group('backtrack').replace('\"', '')

        macro = self.macro_factory.get_macro('room')(name, start, right, left, back, backtrack)
        return macro


class EndpointMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(endpoint:"

    def parse(self, text):
        match = self.compiled.match(text)

        room = match.group('room').replace('\"', '')
        direction = match.group('direction').replace('\"', '')

        macro = self.macro_factory.get_macro('endpoint')(room, direction)
        return macro


class BacktrackMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(backtrack:"

    def parse(self, text):
        match = self.compiled.match(text)
        room = match.group('room').replace('\"', '')
        macro = self.macro_factory.get_macro('backtrack')(room)
        return macro


class TrialMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(trial:"

    def parse(self, text):
        match = self.compiled.match(text)

        risk_type = match.group('risk_type').replace('\"', '')
        id = match.group('id')
        sequence = match.group('sequence')

        macro = self.macro_factory.get_macro('trial')(risk_type, id, sequence)
        return macro


class ImageMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(image:"

    def parse(self, text):
        match = self.compiled.match(text)
        name = match.group('name').replace('\"', '')
        macro = self.macro_factory.get_macro('image')(name)
        return macro


class PlaySoundMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(playSound:"

    def parse(self, text):
        match = self.compiled.match(text)
        event = match.group('event').replace('\"', '')
        mode = match.group('mode').replace('\"', '')
        macro = self.macro_factory.get_macro('playSound')(event, mode)
        return macro


class CreateSoundMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(sound:"

    def parse(self, text):
        match = self.compiled.match(text)
        name = match.group('name').replace('\"', '')
        event = match.group('event').replace('\"', '')
        macro = self.macro_factory.get_macro('sound')(name, event)
        return macro


class CountdownMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(countdown:"

    def parse(self, text):
        match = self.compiled.match(text)
        seconds = int(match.group('seconds'))
        event = match.group('event').replace('\"', '')
        timeout_passage = match.group('timeout_passage').replace('\"', '')
        macro = self.macro_factory.get_macro('countdown')(seconds, event, timeout_passage)
        return macro


class ExecMacroParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(exec:"

    def parse(self, text):
        match = self.compiled.match(text)
        command = match.group('command').replace('\"', '')
        macro = self.macro_factory.get_macro('exec')(command)
        return macro


class PoseParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(pose:"

    def parse(self, text):
        match = self.compiled.match(text)
        name = match.group('name').replace('\"', '')
        macro = self.macro_factory.get_macro('pose')(name)
        return macro


class SayParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(say:"

    def parse(self, text):
        match = self.compiled.match(text)
        sentence = match.group('sentence').replace('\"', '')
        try:
            emotion = match.group('emotion').replace('\"', '')
        except:
            emotion = ""

            
        macro = self.macro_factory.get_macro('say')(sentence, emotion)
        return macro


class FeelParser(MacroParser):
    def __init__(self,regex):
        MacroParser.__init__(self, regex)
        self.incipt = "(feel:"

    def parse(self, text):
        match = self.compiled.match(text)
        emotion = match.group('emotion').replace('\"', '')
        macro = self.macro_factory.get_macro('feel')(emotion)
        return macro


# class IfMacroParser(MacroParser):
#     def __init__(self,regex):
#         MacroParser.__init__(self, regex)
#         self.incipt = "(if:"
#
#     def parse(self, text):
#         match = self.compiled.match(text)
#
#         checkVar = match.group('checkVar')
#         value = match.group('value')
#         text = match.group('text')
#
#         macro = self.macro_factory.get_macro('if')(checkVar, value, text)
#
#         return macro


