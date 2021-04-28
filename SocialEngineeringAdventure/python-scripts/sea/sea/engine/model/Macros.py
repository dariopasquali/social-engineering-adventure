import math

import markdown

from sea.engine.model.Enemy import Enemy
from sea.engine.model.Item import Item


class MacroFactory:

    def __init__(self):
        self.macros = {
            'set': SetMacro,
            'setVarVar': SetVarVarMacro,
            'add': AddMacro,
            'sub': SubMacro,
            'addVarVar': AddVarVarMacro,
            'subVarVar': SubVarVarMacro,
            'haveConsumable': HaveConsumableMacro,
            'addConsumable': AddConsumableMacro,
            'addConsumableVarVar': AddConsumableVarVarMacro,
            'haveItem': HaveItemMacro,
            'addItem': AddItemMacro,
            'gain': GainMacro,
            'pay': PayMacro,
            'equip': EquipMacro,
            'use': UseMacro,
            'useConsumable': UseConsumableMacro,
            'fight': FightMacro,
            'heal': HealMacro,
            'hit': HitMacro,
            'roll': RollMacro,
            'enemy': CreateEnemyMacro,
            'item': CreateItemMacro,
            'link': LinkMacro,
            # 'if': IfMacro

            'room': RoomMacro,
            'endpoint': EndpointMacro,
            'trial': TrialMacro,
            'backtrack': BacktrackMacro,
            'image': ImageMacro,
            'playSound': PlaySoundMacro,
            'sound': CreateSoundMacro,

            'countdown': CountdownMacro,
            'exec': ExecMacro,

            'pose': PoseMacro,
            'say': SayMacro,
            'feel': FeelMacro,
            'fail': FailMacro,
        }
        pass

    def get_macro(self, type):
        return self.macros[type]


class HarloweMacro:

    def __init__(self):
        pass

    def exec(self, env):
        # print("Not implemented")
        return env

    def getType(self):
        return None


# region EXPERIMENT_MACRO

class LinkMacro(HarloweMacro):
    def __init__(self, text=None, toPassage=None):
        HarloweMacro.__init__(self)
        self.text = text
        self.toPassage = toPassage

    def __str__(self):
        return "Link| {} -> {}".format(self.text, self.toPassage)

    def to_json(self):
        return {'cmd': 'link', 'text': self.text, 'toPassage': self.toPassage}

    def getType(self):
        return "link"


class RoomMacro(HarloweMacro):
    def __init__(self, name=None, start=None, right=None, left=None, back=None, backtrack=None):
        HarloweMacro.__init__(self)
        self.name = name
        self.start = start
        self.right = right
        self.left = left
        self.back = back
        self.backtrack = backtrack

    def __str__(self):
        return "Room| name:{}, start:{}, right:{}, left:{}, back:{}, backtrack:{}".format(self.name, self.start,
                                                                                          self.right, self.left,
                                                                                          self.back, self.backtrack)

    def to_json(self):
        return {'cmd': 'room', 'name': self.name, 'start': self.start, 'right': self.right, 'left': self.left,
                'back': self.back, 'backtrack': self.backtrack}

    def getType(self):
        return "room"


class EndpointMacro(HarloweMacro):
    def __init__(self, room=None, direction=None):
        HarloweMacro.__init__(self)
        self.room = room
        self.direction = direction

    def __str__(self):
        return "Endpoint| room:{}, direction:{}".format(self.room, self.direction)

    def to_json(self):
        return {'cmd': 'endpoint', 'room': self.room, 'direction': self.direction}

    def getType(self):
        return "endpoint"


class TrialMacro(HarloweMacro):
    def __init__(self, risk_type=None, id=None, sequence=None):
        HarloweMacro.__init__(self)
        self.risk_type = risk_type
        self.id = id
        self.sequence = sequence

    def __str__(self):
        return "Trial| risk_type:{}, id:{}, sequence:{}".format(self.risk_type, self.id, self.sequence)

    def to_json(self):
        return {'cmd': 'trial', 'risk_type': self.risk_type, 'id': self.id, 'sequence': self.sequence}

    def getType(self):
        return "trial"


class BacktrackMacro(HarloweMacro):
    def __init__(self, room=None):
        HarloweMacro.__init__(self)
        self.room = room

    def __str__(self):
        return "Backtrack| room:{},".format(self.room)

    def to_json(self):
        return {'cmd': 'backtrack', 'room': self.room}

    def getType(self):
        return "backtrack"


# endregion

# region RESOURCES_MACRO (heal, hit, gain, pay)

class HealMacro(HarloweMacro):
    def __init__(self, hp=None):
        HarloweMacro.__init__(self)
        self.hp = hp

    def exec(self, env):
        if type(self.hp) is str:
            if "$" in self.hp:
                val = env[self.hp.replace("$", "")]
            else:
                val = int(self.hp)
            env['hp'] += val
        else:
            env['hp'] += self.hp

        env['eq_sub_1'] = env['hp'] - 1
        env['eq_sub_1_half'] = math.floor(env['eq_sub_1'] / 2)

        env['soundToPlay'] = env['sounds']['heal']
        env['playSoundMode'] = 'once'
        env['playSound'] = True

        return env

    def __str__(self):
        return "(heal: {})".format(self.hp)

    def to_json(self):
        return {'cmd': 'heal', 'hp': self.hp}


class HitMacro(HarloweMacro):
    def __init__(self, dmg=None):
        HarloweMacro.__init__(self)
        self.dmg = dmg

    def exec(self, env):
        if type(self.dmg) is str:
            if "$" in self.dmg:
                val = env[self.dmg.replace("$", "")]
            else:
                val = int(self.dmg)
            env['hp'] -= val
        else:
            env['hp'] -= self.dmg

        env['eq_sub_1'] = env['hp'] - 1
        env['eq_sub_1_half'] = math.floor(env['eq_sub_1'] / 2)

        env['soundToPlay'] = env['sounds']['hit']
        env['playSoundMode'] = 'once'
        env['playSound'] = True

        return env

    def __str__(self):
        return "(hit: {})".format(self.dmg)

    def to_json(self):
        return {'cmd': 'hit', 'dmg': self.dmg}


class GainMacro(HarloweMacro):
    def __init__(self, money=None):
        HarloweMacro.__init__(self)
        self.money = money

    def exec(self, env):
        if type(self.money) is str:
            if "$" in self.money:
                val = env[self.money.replace("$", "")]
            else:
                val = int(self.money)
            env['money'] += val
        else:
            env['money'] += self.money
        return env

    def __str__(self):
        return "(gain: {})".format(self.money)

    def to_json(self):
        return {'cmd': 'gain', 'money': self.money}


class PayMacro(HarloweMacro):
    def __init__(self, money=None):
        HarloweMacro.__init__(self)
        self.money = money

    def exec(self, env):
        if type(self.money) is str:
            if "$" in self.money:
                val = env[self.money.replace("$", "")]
            else:
                val = int(self.money)
            env['money'] -= val
        else:
            env['money'] -= self.money
        return env

    def __str__(self):
        return "(pay: {})".format(self.money)

    def to_json(self):
        return {'cmd': 'pay', 'money': self.money}


# endregion

# region INVENTORY_MACRO (add/have/use item)


class UseMacro(HarloweMacro):
    def __init__(self, item=None):
        HarloweMacro.__init__(self)
        self.item = item

    def exec(self, env):
        if env['inventory'][self.item].is_consumable:
            qta_check = env['inventory'][self.item].use()
            if not qta_check:
                del env['inventory'][self.item]
        else:
            del env['inventory'][self.item]

        return env

    def __str__(self):
        return "(use: {})".format(self.item)

    def to_json(self):
        return {'cmd': 'use', 'item': self.item}


class HaveItemMacro(HarloweMacro):
    def __init__(self, item=None, linkID=None):
        HarloweMacro.__init__(self)
        self.item = item
        self.linkID = linkID

    def exec(self, env):
        env['checkResult'] = (self.item in env['inventory'], self.linkID)
        return env

    def __str__(self):
        return "(haveItem: {}, {})".format(self.item, self.linkID)

    def to_json(self):
        return {'cmd': 'haveItem', 'item': self.item, 'linkID': self.linkID}


class HaveConsumableMacro(HarloweMacro):
    def __init__(self, consumable=None, resultVar=None):
        HarloweMacro.__init__(self)
        self.consumable = consumable
        self.resultVar = resultVar

    def exec(self, env):
        env['checkResult'] = self.consumable in env['inventory'] and env['inventory'][self.consumable].qta > 0
        return env

    def __str__(self):
        return "(haveConsumable: {}, ${})".format(self.consumable, self.resultVar)

    def to_json(self):
        return {'cmd': 'haveConsumable', 'consumable': self.consumable, 'resultVar': self.resultVar}


class AddItemMacro(HarloweMacro):
    def __init__(self, item=None):
        HarloweMacro.__init__(self)
        self.item = item

    def exec(self, env):
        env['inventory'][self.item] = env['items'][self.item]
        return env

    def __str__(self):
        return "(addItem: {})".format(self.item)

    def to_json(self):
        return {'cmd': 'addItem', 'item': self.item}


class AddConsumableMacro(HarloweMacro):
    def __init__(self, consumable=None, qta=None):
        HarloweMacro.__init__(self)
        self.consumable = consumable
        self.qta = int(qta)

    def exec(self, env):
        if self.consumable in env['inventory']:
            env['inventory'][self.consumable].add(self.qta)
        else:
            env['inventory'][self.consumable] = env['items'][self.consumable]
            env['inventory'][self.consumable].set_qta(self.qta)
        return env

    def __str__(self):
        return "(addConsumable: {}, {})".format(self.consumable, self.qta)

    def to_json(self):
        return {'cmd': 'addConsumable', 'consumable': self.consumable, 'qta': self.qta}


class CreateItemMacro(HarloweMacro):
    def __init__(self, name=None, type=None, effect=None, value=None):
        HarloweMacro.__init__(self)
        self.name = name
        self.type = type
        self.effect = effect
        self.value = value
        self.passage_name = ""

    def exec(self, env):

        if 'items' not in env:
            env['items'] = {}

        if self.name not in env['items']:
            is_cons = self.type == 'cons'
            env['items'][self.name] = Item(self.name, self.effect, is_cons, self.value, self.passage_name)
        return env

    def __str__(self):
        return "(item: {}, {}, {}, {})".format(self.name, self.type, self.effect, self.value)

    def to_json(self):
        return {'cmd': 'createItem', 'name': self.name, 'type': self.type, 'effect': self.effect, 'value': self.value}


# endregion

# region TRIALS_MACRO (fight, roll)

class CreateEnemyMacro(HarloweMacro):
    def __init__(self, name=None, defense=None, dmg=None):
        HarloweMacro.__init__(self)
        self.name = name
        self.dmg = dmg
        self.defense = defense

    def exec(self, env):

        if 'enemies' not in env:
            env['enemies'] = {}

        if self.name not in env['enemies']:
            env['enemies'][self.name] = Enemy(self.name, self.defense, self.dmg)
        return env

    def __str__(self):
        return "(enemy: {}, {}, {})".format(self.name, self.defense, self.dmg)

    def to_json(self):
        return {'cmd': 'createEnemy', 'name': self.name, 'defense': self.defense, 'dmg': self.dmg}


class FightMacro(HarloweMacro):
    def __init__(self, enemy=None):
        HarloweMacro.__init__(self)
        self.enemy = enemy

    def exec(self, env):
        enemy = env['enemies'][self.enemy]
        env['enemyName'] = enemy.name
        env['enemyDmg'] = enemy.dmg
        env['enemyDef'] = enemy.defense
        # env['rollResult'] = env['dice'].roll() >= enemy.defense
        return env

    def __str__(self):
        return "(fight: {})".format(self.enemy)

    def to_json(self):
        return {'cmd': 'fight', 'enemy': self.enemy}


class RollMacro(HarloweMacro):
    def __init__(self, cd=None):
        HarloweMacro.__init__(self)
        self.cd = cd

    def exec(self, env):
        env['rollCD'] = int(self.cd)
        # env['rollResult'] = env['dice'].roll() >= int(self.cd)
        return env

    def __str__(self):
        return "(roll: {})".format(self.cd)

    def to_json(self):
        return {'cmd': 'roll', 'cd': self.cd}


class FailMacro(HarloweMacro):
    def __init__(self):
        HarloweMacro.__init__(self)

    def exec(self, env):
        env['failRoll'] = True
        return env

    def __str__(self):
        return "(fail:)"

    def to_json(self):
        return {'cmd': 'fail'}


# endregion

# region IMMERSION_MACROS (image and sound)

class ImageMacro(HarloweMacro):
    def __init__(self, name=None):
        HarloweMacro.__init__(self)
        self.name = name

    def exec(self, env):
        env['image'] = self.name
        return env

    def __str__(self):
        return "(image: {})".format(self.name)

    def to_json(self):
        return {'cmd': 'image', 'image': self.name}


class CreateSoundMacro(HarloweMacro):
    def __init__(self, name=None, event=None):
        HarloweMacro.__init__(self)
        self.name = name
        self.event = event

    def exec(self, env):
        if 'sounds' not in env:
            env['sounds'] = {}

        env['sounds'][self.event] = self.name
        return env

    def __str__(self):
        return "(sound: {} {})".format(self.name, self.event)

    def to_json(self):
        return {'cmd': 'sound', 'name': self.name, 'event': self.event}


class PlaySoundMacro(HarloweMacro):
    def __init__(self, event=None, mode=None):
        HarloweMacro.__init__(self)
        self.event = event
        self.mode = mode

    def exec(self, env):

        if self.event in env['sounds']:
            env['soundToPlay'] = env['sounds'][self.event]
            env['playSoundMode'] = self.mode
            env['playSound'] = True
        else:
            env['playSound'] = False
        return env

    def __str__(self):
        return "(sound: {} {})".format(self.event, self.mode)

    def to_json(self):
        return {'cmd': 'sound', 'event': self.event, 'mode': self.mode}


# endregion

# region EXPERIMENT_MACRO (countdown, execute)

class CountdownMacro(HarloweMacro):
    def __init__(self, seconds=0, event="", timeout_passage=""):
        HarloweMacro.__init__(self)
        self.seconds = seconds
        self.event = event
        self.timeout_passage = timeout_passage

    def exec(self, env):
        env['countdown_seconds'] = self.seconds
        env['timeout_passage'] = self.timeout_passage
        return env

    def __str__(self):
        return "(countdown: {}, {}, {})".format(self.seconds, self.event, self.timeout_passage)

    def to_json(self):
        return {'cmd': 'countdown', 'seconds': self.seconds, 'event': self.event,
                'timeout_passage': self.timeout_passage}


class PoseMacro(HarloweMacro):
    def __init__(self, name=None):
        HarloweMacro.__init__(self)
        self.name = name

    def __str__(self):
        return "(pose: {})".format(self.name)

    def to_json(self):
        return {'cmd': 'pose', 'name': self.name}


class SayMacro(HarloweMacro):
    def __init__(self, sentence=None, emotion=""):
        HarloweMacro.__init__(self)
        self.sentence = sentence
        self.sentence_rendered = ""
        self.emotion = emotion

    def exec(self, env):
        self.sentence_rendered = self.sentence
        if env['lang'] == "eng":
            self.sentence_rendered = env["translator"].translate(self.sentence_rendered, dest='en')

    def __str__(self):
        return "(say: {}, {})".format(self.sentence, self.emotion)

    def to_json(self):
        return {'cmd': 'say', 'sentence': self.sentence, 'emotion': self.emotion}


class FeelMacro(HarloweMacro):
    def __init__(self, emotion=None):
        HarloweMacro.__init__(self)
        self.emotion = emotion

    def __str__(self):
        return "(feel: {})".format(self.emotion)

    def to_json(self):
        return {'cmd': 'feel', 'emotion': self.emotion}


class ExecMacro(HarloweMacro):
    def __init__(self, command=None):
        HarloweMacro.__init__(self)
        self.command = command

    def exec(self, env):
        env['command'] = self.command
        env['command_running'] = False
        return env

    def __str__(self):
        return "(exec: {})".format(self.command)

    def to_json(self):
        return {'cmd': 'exec', 'command': self.command}


# endregion


# region USELESS_MACROS

class SetMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def exec(self, env):

        if type(self.right) == str and "$" in self.right:
            val = env[self.right.replace("$", "")]
        else:
            val = self.right

        try:
            env[self.left] = int(val)
        except:
            env[self.left] = val

        return env

    def __str__(self):
        return "(set: {}, {})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'set', 'left': self.left, 'right': self.right}


class SetVarVarMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def exec(self, env):
        env[self.left] = env[self.right]
        return env

    def __str__(self):
        return "(set: {}, ${})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'setVarVar', 'left': self.left, 'right': self.right}


class AddMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def __str__(self):
        return "(set: {}, {})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'add', 'left': self.left, 'right': self.right}


class SubMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def __str__(self):
        return "(set: {}, {})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'sub', 'left': self.left, 'right': self.right}


class AddVarVarMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def __str__(self):
        return "(set: {}, ${})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'addVarVar', 'left': self.left, 'right': self.right}


class SubVarVarMacro(HarloweMacro):
    def __init__(self, left=None, right=None):
        HarloweMacro.__init__(self)
        self.left = left
        self.right = right

    def __str__(self):
        return "(set: {}, ${})".format(self.left, self.right)

    def to_json(self):
        return {'cmd': 'subVarVar', 'left': self.left, 'right': self.right}


class EquipMacro(HarloweMacro):
    def __init__(self, item=None):
        HarloweMacro.__init__(self)
        self.item = item

    def __str__(self):
        return "(equip: {})".format(self.item)

    def to_json(self):
        return {'cmd': 'equip', 'item': self.item}


class AddConsumableVarVarMacro(HarloweMacro):
    def __init__(self, consumable=None, qtaVar=None):
        HarloweMacro.__init__(self)
        self.consumable = consumable
        self.qtaVar = qtaVar

    def __str__(self):
        return "(addConsumableVarVar: {}, ${})".format(self.consumable, self.qtaVar)

    def to_json(self):
        return {'cmd': 'haveConsumable', 'consumable': self.consumable, 'qtaVar': self.qtaVar}


class UseConsumableMacro(HarloweMacro):
    def __init__(self, consumable=None):
        HarloweMacro.__init__(self)
        self.consumable = consumable

    def __str__(self):
        return "(useConsumable: {})".format(self.consumable)

    def to_json(self):
        return {'cmd': 'useConsumable', 'consumable': self.consumable}

# class IfMacro(HarloweMacro, StoryLine):
#     def __init__(self, checkVar=None, value=None, textToShow=None):
#         HarloweMacro.__init__(self)
#         self.checkVar = checkVar
#         self.value = value
#         self.textToShow = textToShow
#
#     def __str__(self):
#         return "if({} == {}) show {}".format(self.checkVar, self.value, self.textToShow)
#
#     def to_json(self):
#         return {'cmd': 'if', 'checkVar': self.checkVar, 'value': self.value, 'textToShow': self.textToShow}

# endregion
