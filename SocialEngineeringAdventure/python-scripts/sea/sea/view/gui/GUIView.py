"""
Methods to play the story via GUI
"""
import os
import sys
from enum import Enum

import markdown

from sea.engine.model.Macros import FeelMacro, PoseMacro, SayMacro
from sea.engine.model.Passage import PassageType, BodyType, BodyLineType
from sea.engine.model.StoryLine import StoryLine
from sea.view.SoundPlayer import SoundPlayer
from sea.view.gui.StatsBridge import StatsBridge
from sea.view.gui.StoryBridge import StoryBridge
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QTimer, Signal, Property

from screeninfo import get_monitors

from functools import partial



class RollType(Enum):
    DICE = 0
    ATTACK = 1


def get_screen_info(display_id=1):
    width = 0
    height = 0
    name_pattern = "DISPLAY" + str(display_id)

    for m in get_monitors():
        if name_pattern in m.name:
            width = m.width
            height = m.height

    return width, height


ANNOTATION_ROOM = "ROOM"
ANNOTATION_PASSAGE = "PASSAGE"
ANNOTATION_RENDERING = "RENDERING"
ANNOTATION_START = "START"
ANNOTATION_END = "END"

ANNOTATION_CONTINUE = "CONTINUE"
ANNOTATION_DECISION = "DECISION"
ANNOTATION_DECISION_RIGHT = "RIGHT"
ANNOTATION_DECISION_LEFT = "LEFT"
ANNOTATION_DECISION_CENTRE = "CENTRE"

ANNOTATION_DICE = "DICE"
ANNOTATION_COUNTDOWN = "COUNTDOWN"

ANNOTATION_EXTRA_LIFE = "EXTRA_LIFE"
ANNOTATION_GLOVE = "GLOVE"


class GUIView:

    def __init__(self, sea_engine, experimental_utils, monitor_id=2, with_sound=True, lang='ita'):

        self.experimental_utils = experimental_utils

        self.sea_engine = sea_engine
        self.continue_link = None
        self.right_link = None
        self.left_link = None
        self.centre_link = None

        self.choice = None

        self.interactive_body = None
        self.wait_puppet_ack = True

        self.check_result = False
        self.dice_result = -1

        self.timer = None
        self.count = 0
        self.countdown_label = ""

        self.app = None
        self.gui_engine = None

        self.image_path = "../images/"
        self.sound_path = "sea/assets/music"

        # Init Sound
        self.with_sound = with_sound
        if with_sound:
            self.soundplayer = SoundPlayer(self.sound_path)

        # Init monitors
        self.__width, self.__height = get_screen_info(monitor_id)
        width_unit = self.__width / 3
        self.story_view = StoryBridge(width_unit * 2, self.__height)
        self.stats_view = StatsBridge(width_unit, self.__height)

        # Init stats
        self.stats_view.set_update_engine_callback(self.sea_engine.use_item_callback)
        self.stats_view.set_show_item_callback(self.__render_item_callback)
        self.stats_view.set_fetch_stats_callback(self.sea_engine.get_stats)
        self.stats_view.set_image_path(self.image_path)

        # Init rendering
        self.__rendering_map = {
            PassageType.TEXT: self.__render_text_passage,
            PassageType.ENDPOINT: self.__render_endpoint_passage,
            PassageType.BACK: self.__render_back_passage,
            PassageType.BACKTRACK: self.__render_backtrack_passage,
            PassageType.FIGHT: self.__render_fight_passage,
            PassageType.ROLL: self.__render_roll_passage,
            PassageType.TRIAL: self.__render_trial_passage,
            PassageType.ITEM_CHECK: self.__render_item_check_passage,
            PassageType.END: self.__render_end_passage,
            PassageType.COUNTDOWN_START: self.__render_countdown_start_passage,
            PassageType.COUNTDOWN_STOP: self.__render_countdown_stop_passage,
            PassageType.TRIAL_COUNTDOWN_START: self.__render_trial_countdown_start,
        }
        self.__annotation_map = {
            PassageType.TEXT: "TEXT",
            PassageType.ENDPOINT: "ENDPOINT",
            PassageType.BACK: "BACK",
            PassageType.BACKTRACK: "BACKTRACK",
            PassageType.FIGHT: "FIGHT",
            PassageType.ROLL: "ROLL",
            PassageType.TRIAL: "TRIAL",
            PassageType.ITEM_CHECK: "ITEM_CHECK",
            PassageType.END: "END",
            PassageType.COUNTDOWN_START: "COUNTDOWN_START",
            PassageType.COUNTDOWN_STOP: "COUNTDOWN_STOP",
            PassageType.TRIAL_COUNTDOWN_START: "TRIAL_COUNTDOWN_START",
        }

    # region Signals

    # widthChanged = Signal(int)
    # heightChanged = Signal(int)
    #
    # def get_width(self):
    #     return self.__width
    #
    # def get_height(self):
    #     return self.__height
    #
    # width = Property(int, get_width, notify=widthChanged)
    # height = Property(int, get_height, notify=heightChanged)
    #
    # def __notify_view(self):
    #     self.widthChanged.emit(self.__width)
    #     self.heightChanged.emit(self.__height)

    # endregion

    # Initialize the QT GUI and its panels for story and stats
    def init_gui_engine(self):
        self.app = QGuiApplication(sys.argv)
        self.gui_engine = QQmlApplicationEngine()
        # self.gui_engine.rootContext().setContextProperty("mainBridge", self)
        self.gui_engine.rootContext().setContextProperty("storyBridge", self.story_view)
        self.gui_engine.rootContext().setContextProperty("statsBridge", self.stats_view)
        self.gui_engine.load(os.path.join("sea/assets/gui/main.qml"))

        # Check the GUI is loaded
        if not self.gui_engine.rootObjects():
            return

        # Annotate the begin of the experiment
        self.experimental_utils.annotate([ANNOTATION_ROOM, ANNOTATION_START, self.sea_engine.get_current_room_name()])

        # If the app is correctly loaded, I can render the first passage
        # self.experimental_utils.log("ROOM_SEQ {}".format(self.sea_engine.get_current_room_name()))
        self.render_current_passage()

        return self.app

    # region PASSAGE RENDERING ENTRYPOINT

    # Entrypoint method to render a passage based on its type
    def render_current_passage(self):

        self.sea_engine.check_extra_life()

        if not (self.sea_engine.is_running and self.sea_engine.is_alive()):
            if self.sea_engine.check_and_use_special_effects("extra_life"):
                self.render_resurrection()
                return
            else:
                self.render_death()
                return

        # Reset the Story Text
        self.story_view.set_story_line("")

        # Update/Play Sound
        if self.with_sound:
            sound_play, sound_track, sound_mode = self.sea_engine.get_sound()
            if sound_play:
                self.soundplayer.play(sound_track, sound_mode)

        # Update the Stats Panel
        self.stats_view.update(self.sea_engine.get_hp(), self.sea_engine.get_power(), self.sea_engine.get_inventory())
        self.stats_view.set_image(self.sea_engine.get_image())
        self.stats_view.show_image()

        # Render the next passage (tail_recursive)
        passage = self.sea_engine.current_passage
        self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_START, passage.name,
                                          self.__annotation_map[passage.passage_type],
                                          self.sea_engine.get_hp(), self.sea_engine.get_power()])

        self.__passage_rendering_entrypoint(passage)

    # Update the internal state of the SEA engine and trigger the passage rendering
    def __render_next_passage(self, specific_passage=None):

        if self.choice is None:
            return

        # Update the current passage based on the choice
        if specific_passage is not None:
            self.sea_engine.next_passage(specific_passage)
        else:
            next_p = self.choice.toPassage
            self.sea_engine.next_passage(next_p)

        # Clear the choices
        self.continue_link = None
        self.right_link = None
        self.left_link = None
        self.centre_link = None

        # Then render it
        self.render_current_passage()

    # endregion

    # region ENDING

    def end_game(self):
        # Ends the experiment and stops the devices
        self.experimental_utils.end_experiment()
        # Eventually run the Questionnaire #TODO
        self.app.quit()

    def render_resurrection(self):

        self.experimental_utils.annotate([ANNOTATION_EXTRA_LIFE])
        passage = self.sea_engine.get_passage("extra_life")
        self.sea_engine.set_hp(10)

        self.story_view.set_story_line("")
        self.__show_body(passage)
        self.story_view.set_btn_continue_txt("Continua")
        self.story_view.set_continue_callback(self.render_current_passage)
        self.story_view.set_btn_continue_visible(True)
        self.story_view.hide_choice()

    def render_death(self):
        passage = self.sea_engine.get_passage("death")
        self.sea_engine.set_hp(0)

        self.story_view.set_story_line("")
        self.__show_body(passage)
        self.story_view.set_btn_continue_txt("Fine")
        self.story_view.set_continue_callback(self.end_game)
        self.story_view.set_btn_continue_visible(True)
        self.story_view.hide_choice()

    # endregion

    # region CALLBACKS

    def __continue_choice_callback(self):

        passage = self.sea_engine.current_passage

        self.experimental_utils.annotate([ANNOTATION_CONTINUE])

        # No choice to make, so the passage is ended
        if self.right_link is None:
            self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_END])
            self.choice = self.continue_link
            self.__render_next_passage()
        else:
            # Show the choices
            self.story_view.set_btn_continue_visible(False)
            self.story_view.show_choice()

            if self.centre_link is not None:
                self.story_view.set_btn_centre_visible(True)

    def __right_choice_callback(self):
        self.experimental_utils.annotate([ANNOTATION_DECISION, ANNOTATION_DECISION_RIGHT, self.right_link.toPassage])
        self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_END])
        self.choice = self.right_link
        self.__render_next_passage()

    def __left_choice_callback(self):
        self.experimental_utils.annotate([ANNOTATION_DECISION, ANNOTATION_DECISION_LEFT, self.left_link.toPassage])
        self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_END])
        self.choice = self.left_link
        self.__render_next_passage()

    def __centre_choice_callback(self):
        self.experimental_utils.annotate([ANNOTATION_DECISION, ANNOTATION_DECISION_CENTRE, self.centre_link.toPassage])
        self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_END])
        self.choice = self.centre_link
        self.__render_next_passage()

    def __roll_callback(self):
        self.story_view.append_story_line("<p><b>Hai fatto {}!</b></p>".format(self.dice_result))
        self.story_view.set_btn_continue_txt("Continua")

        if self.sea_engine.check_and_use_special_effects("win"):
            passage = self.sea_engine.get_passage("win", render=True)
            self.story_view.set_story_line("")
            self.__show_body(passage)
            self.check_result = True
            self.experimental_utils.annotate([ANNOTATION_GLOVE])

        if self.check_result:
            # Success
            self.choice = self.right_link
            decision = ANNOTATION_DECISION_RIGHT
        else:
            # Fail
            self.choice = self.left_link
            decision = ANNOTATION_DECISION_LEFT

        self.experimental_utils.annotate([ANNOTATION_DECISION, decision])
        self.experimental_utils.annotate([ANNOTATION_PASSAGE, ANNOTATION_END])

        # Just render the next passage
        self.story_view.set_continue_callback(self.__render_next_passage)

    def __have_item_callback(self):
        passage = self.sea_engine.current_passage
        self.__show_alternatives(passage)

        (check_result, link_id) = self.sea_engine.check_have_item()

        self.story_view.set_btn_continue_visible(False)
        self.story_view.show_choice()

        if check_result:
            self.story_view.set_btn_left_enabled(False)
        else:
            self.story_view.set_btn_right_enabled(False)

    def __trial_callback(self):

        passage = self.sea_engine.current_passage

        # Show the choices
        self.story_view.set_btn_continue_visible(False)
        self.story_view.show_choice()

    def __trial_countdown_callback(self):

        passage = self.sea_engine.current_passage
        self.__show_body(passage)

        # Show the choices
        self.story_view.set_btn_continue_visible(False)
        self.story_view.show_choice()

        # Start the Countdown
        self.count, timeout_passage = self.sea_engine.get_countdown()
        partial_countdown = partial(self.__countdown_and_update_view, timeout_passage, True)
        self.__start_countdown(partial_countdown)

    def __right_trial_choice_callback(self):
        passage = self.sea_engine.current_passage

        # self.experimental_utils.annotate(self.sea_engine.current_passage.name,
        #                                  hp=self.sea_engine.get_hp(), power=self.sea_engine.get_power(),
        #                                  event=ANNOTATION_EVENT_DECISION, trial_type=passage.trial_type,
        #                                  trial_id=passage.trial_id, trial_seq=passage.trial_seq,
        #                                  decision="R")
        self.choice = self.right_link
        self.__render_next_passage()

    def __left_trial_choice_callback(self):
        passage = self.sea_engine.current_passage

        # self.experimental_utils.annotate(self.sea_engine.current_passage.name,
        #                                  hp=self.sea_engine.get_hp(), power=self.sea_engine.get_power(),
        #                                  event=ANNOTATION_EVENT_DECISION, trial_type=passage.trial_type,
        #                                  trial_id=passage.trial_id, trial_seq=passage.trial_seq,
        #                                  decision="L")
        self.choice = self.left_link
        self.__render_next_passage()

    def __use_item_callback(self, item):
        self.sea_engine.use_item_callback(item.name)
        self.render_current_passage()
        pass

    def __render_item_callback(self, item_name):
        item = self.sea_engine.get_item(item_name)
        passage = self.sea_engine.get_passage(item.passage_name, render=True)
        casted_use_item_callback = partial(self.__use_item_callback, item)

        item_body = ""

        for _, (blt, line, blt_next) in passage.create_linked_body_lines().items():
            if type(line) == StoryLine:
                item_body += str(line) + "<br>"

        self.stats_view.set_object_description(item_body)


    # endregion

    # region PASSAGE RENDERING

    def __passage_rendering_entrypoint(self, passage=None):

        if passage is None:
            passage = self.sea_engine.current_passage

        if self.interactive_body is None:
            # We just started the recursive rendering
            self.experimental_utils.annotate([
                ANNOTATION_RENDERING, ANNOTATION_START
            ])

        self.__rendering_map[passage.passage_type](passage)

    def __parse_exec_body_line(self, line):
        robot = self.experimental_utils.get_robot()

        if type(line) == StoryLine:
            self.story_view.append_story_line(str(line))

        if type(line) == PoseMacro:
            if robot is not None:
                robot.pose_async(line.name)  # Blocking for a second

        if type(line) == SayMacro:
            if robot is not None:
                robot.say_async(line.sentence, line.emotion)  # Blocking for a second
            self.story_view.append_story_line("<p> iCub: <i>" + str(line.sentence_rendered) + "</i></p>")

        if type(line) == FeelMacro:
            if robot is not None:
                robot.feel_async(line.emotion)  # Blocking for a second

        return robot is not None

    def __show_body_legacy(self, body_lines):
        for _, (blt, line, blt_next) in body_lines.items():
            if type(line) == StoryLine:
                self.story_view.append_story_line(str(line))

            if type(line) == SayMacro:
                self.story_view.append_story_line("<p> iCub: <i>" + str(line.sentence_rendered) + "</i></p>")

        return True

    def __show_body(self, passage=None, force_no_robot=False):

        self.experimental_utils.log("show body")
        # If I force no robot the show body just renders the text
        # Used with debugging and item ? button
        have_robot = (self.experimental_utils.get_robot() is not None) and (not force_no_robot)

        if self.interactive_body is not None:
            body_lines = self.interactive_body
        else:
            if passage is None:
                return True
            else:
                body_lines = passage.create_linked_body_lines()

        if not have_robot:
            return self.__show_body_legacy(body_lines)
        else:
            if len(body_lines) == 0:
                self.experimental_utils.log(
                    "I have no more body lines, let's exit the loop and render the alternatives")
                # if it was the last line
                # Stop the recursion
                # And show the alternatives
                self.interactive_body = None
                self.story_view.set_btn_continue_visible(True)
                self.experimental_utils.annotate([
                    ANNOTATION_RENDERING, ANNOTATION_END
                ])
                return True

            # Do what yo have to do
            _, (blt, line, blt_next) = body_lines.popitem(last=False)
            self.experimental_utils.log("Line Fetched {}".format(line))
            self.experimental_utils.log("Next line type {}".format(blt_next))
            self.__parse_exec_body_line(line)

            self.experimental_utils.log("I have more lines. Set the recursion")

            # Store the remaining of the body
            self.interactive_body = body_lines

            if len(body_lines) == 0:
                self.experimental_utils.log(
                    "I have no more body lines, let's exit the loop and render the alternatives")
                # if it was the last line
                # Stop the recursion
                # And show the alternatives
                self.interactive_body = None
                self.story_view.set_btn_continue_visible(True)
                self.experimental_utils.annotate([
                    ANNOTATION_RENDERING, ANNOTATION_END
                ])
                return True

            # Switch the behavior based on the sequence
            # text -> text = recursion
            # text -> robot = show a continue, wait for user interaction, recursion
            # robot -> * = wait until cmd ack, recursion

            if blt == BodyLineType.TEXT:

                if blt_next == BodyLineType.TEXT or blt_next == BodyLineType.EMPTY:  # text -> text
                    self.experimental_utils.log("text -> text")
                    self.story_view.set_btn_continue_visible(True)
                    return self.__show_body(passage)  # direct recursion

                else:  # text -> robot
                    self.experimental_utils.log("text -> robot, wait for an interaction")
                    # Wait for an user interaction
                    self.story_view.set_btn_continue_txt("Continua")
                    self.story_view.set_btn_continue_visible(True)
                    self.story_view.hide_choice()
                    must_show_alternatives = False
                    self.story_view.set_continue_callback(self.__passage_rendering_entrypoint)  # callback recursion

            else:  # robot -> text/robot

                self.experimental_utils.log("robot -> robot, wait for the end of the command")

                if have_robot:
                    # If I have a robot, what I have to do is just set the callback method
                    # When anything arrives on the ack port, it will trigger the recursion
                    # I know, it is a recursion hell without any main method and with not straight forward flow
                    # welcome to my mind bro
                    self.story_view.set_btn_continue_visible(False)
                    self.story_view.hide_choice()
                    must_show_alternatives = False
                    # callback recursion
                    self.experimental_utils.get_robot().set_ack_port_callback(self.__passage_rendering_entrypoint)
                else:
                    must_show_alternatives = self.__show_body()  # direct recursion

            if must_show_alternatives:
                self.experimental_utils.annotate([
                    ANNOTATION_RENDERING, ANNOTATION_END
                ])

            return must_show_alternatives

    def __show_alternatives(self, passage):

        print("SHOW THE ALTERNATIVES!!")
        links = passage.links

        if len(links) == 1:
            self.continue_link = links[0]
            self.story_view.set_btn_continue_txt(self.continue_link.text)
        else:
            self.story_view.set_btn_continue_txt("Continua")

        self.story_view.set_continue_callback(self.__continue_choice_callback)
        # Hide the two buttons and show the continue one
        self.story_view.set_btn_continue_visible(True)
        self.story_view.hide_choice()

        if len(links) > 1:

            random_position = self.sea_engine.roll_random()
            if random_position >= 10:
                left_link_id = 1
                right_link_id = 0
            else:
                left_link_id = 0
                right_link_id = 1

            self.right_link = links[right_link_id]
            self.story_view.set_btn_right_txt(self.right_link.text)
            self.story_view.set_right_callback(self.__right_choice_callback)

            self.left_link = links[left_link_id]
            self.story_view.set_btn_left_txt(self.left_link.text)
            self.story_view.set_left_callback(self.__left_choice_callback)

            if len(links) == 3:
                self.centre_link = links[2]
                self.story_view.set_btn_centre_txt(self.centre_link.text)
                self.story_view.set_centre_callback(self.__centre_choice_callback)

    # Render a normal text passage
    def __render_text_passage(self, passage=None):
        if self.__show_body(passage):
            self.__show_alternatives(passage)

    # Render an endpoint passage
    def __render_endpoint_passage(self, passage):
        if self.__show_body(passage):
            # Update the internal state
            self.experimental_utils.annotate([ANNOTATION_ROOM, ANNOTATION_END])
            self.sea_engine.next_room()
            self.experimental_utils.annotate(
                [ANNOTATION_ROOM, ANNOTATION_START, self.sea_engine.get_current_room_name()])

            # Wait for an interaction
            self.story_view.hide_choice()
            self.story_view.set_btn_continue_visible(True)
            self.story_view.set_btn_continue_txt("Continua")
            self.story_view.set_continue_callback(self.render_current_passage)

    # handles the dice-roll of fight and roll passages
    def __handle_roll(self, passage, roll_type):
        self.story_view.set_btn_continue_txt("Lancia il Dado!")
        self.story_view.set_continue_callback(self.__roll_callback)

        if roll_type == RollType.ATTACK:
            self.check_result, self.dice_result_raw, self.dice_result = self.sea_engine.roll_attack_and_check()
        elif roll_type == RollType.DICE:
            self.check_result, self.dice_result_raw, self.dice_result = self.sea_engine.roll_dice_and_check()

        self.experimental_utils.annotate([ANNOTATION_DICE, self.check_result, self.dice_result_raw, self.dice_result])
        self.right_link = passage.links[0]
        self.left_link = passage.links[1]

        # Hide the two buttons and show the continue one
        self.story_view.set_btn_continue_visible(True)
        self.story_view.hide_choice()

    # Render a fight passage with dice rolls
    def __render_fight_passage(self, passage):
        if self.__show_body(passage):
            self.__handle_roll(passage, RollType.ATTACK)

    # Render a Roll check passage with dice rolls
    def __render_roll_passage(self, passage):
        if self.__show_body(passage):
            self.__handle_roll(passage, RollType.DICE)

    # Display the trials alternatives and eventually starts a countdown
    def __render_trials_alternatives(self, passage, callback):
        # Annotate the begin of the passage
        self.experimental_utils.annotate([passage.trial_type, passage.trial_id, passage.trial_seq])

        # Handle Trial
        self.story_view.set_btn_continue_txt("Continua")  # TODO
        self.story_view.set_continue_callback(callback)

        random_position = self.sea_engine.roll_random()
        if random_position >= 10:
            left_link_id = 1
            right_link_id = 0
        else:
            left_link_id = 0
            right_link_id = 1

        self.right_link = passage.links[right_link_id]
        self.story_view.set_btn_right_txt(self.right_link.text)
        self.story_view.set_right_callback(self.__right_trial_choice_callback)

        self.left_link = passage.links[left_link_id]
        self.story_view.set_btn_left_txt(self.left_link.text)
        self.story_view.set_left_callback(self.__left_trial_choice_callback)

        # Hide the two buttons and show the continue one
        self.story_view.set_btn_continue_visible(True)
        self.story_view.hide_choice()

    # Render a Trial passage with annotations
    def __render_trial_passage(self, passage):
        if self.__show_body(passage):
            self.experimental_utils.annotate([passage.trial_type, passage.trial_id, passage.trial_seq])
            self.__show_alternatives(passage)

            # self.__render_trials_alternatives(passage, self.__trial_callback)

    # Render a Trial passage with annotations
    def __render_trial_countdown_start(self, passage):
        if self.__show_body(passage):
            self.experimental_utils.annotate([passage.trial_type, passage.trial_id, passage.trial_seq])
            self.__show_alternatives(passage)

            # Start the Countdown
            self.count, timeout_passage = self.sea_engine.get_countdown()
            partial_countdown = partial(self.__countdown_and_update_view, timeout_passage, True)
            self.__start_countdown(partial_countdown)

            # self.__render_trials_alternatives(passage, self.__trial_countdown_callback)

    # Render a back passage, handling the backtracking if possible
    def __render_back_passage(self, passage):

        # Update the room and passage if possible
        if not self.sea_engine.go_back():
            # if I CANNOT go back, just present again the choice
            text = "Purtroppo hai esplorato tutte le strade alternative\n"
            text += "Prosegui! puoi farcela"
            self.story_view.set_story_line(text)

            self.story_view.set_btn_continue_txt("Continua")
            self.story_view.set_continue_callback(self.render_current_passage)
            self.story_view.hide_choice()
            self.story_view.set_btn_continue_visible(True)

        else:
            # if I can go back, the room and passage has been updated
            passage = self.sea_engine.current_passage
            self.__passage_rendering_entrypoint(passage)

    # Render the backtracking passage
    def __render_backtrack_passage(self, passage):
        # Show the current passage
        if self.__show_body(passage):
            # Update the internal state
            self.experimental_utils.annotate([ANNOTATION_ROOM, ANNOTATION_END])
            self.sea_engine.next_room()
            self.experimental_utils.annotate(
                [ANNOTATION_ROOM, ANNOTATION_START, self.sea_engine.get_current_room_name()])

            # Wait for an interaction
            self.story_view.set_btn_continue_txt("Continua")
            self.story_view.set_continue_callback(self.render_current_passage)
            self.story_view.hide_choice()
            self.story_view.set_btn_continue_visible(True)

    # Render an item check passage
    def __render_item_check_passage(self, passage):
        if self.__show_body(passage):
            self.right_link = passage.links[0]
            self.left_link = passage.links[1]

            # Wait for an interaction
            self.story_view.set_btn_continue_txt("Continua")
            self.story_view.set_continue_callback(self.__have_item_callback)
            self.story_view.hide_choice()
            self.story_view.set_btn_continue_visible(True)

    # Render the final passage and close the game
    def __render_end_passage(self, passage):
        if self.__show_body(passage):
            self.sea_engine.end_game()

            # Wait for an interaction
            self.story_view.set_btn_continue_txt("Fine")
            self.story_view.set_continue_callback(self.app.quit)
            self.story_view.hide_choice()
            self.story_view.set_btn_continue_visible(True)

    def __countdown_and_update_view(self, timeout_passage, is_trial=False):
        if self.count < 0:
            self.timer.stop()
            self.__render_next_passage(timeout_passage)
        else:
            self.stats_view.set_countdown("00:{}".format(self.count))
            self.experimental_utils.annotate([ANNOTATION_COUNTDOWN, self.count])
            self.count -= 1

    # Append an increasing countdown to the story line
    # If the countdown ends the story autonomously goes to the failure (second) link
    def __render_countdown_start_passage(self, passage):
        if self.__show_body(passage):
            self.__show_alternatives(passage)

            self.count, timeout_passage = self.sea_engine.get_countdown()
            partial_countdown = partial(self.__countdown_and_update_view, timeout_passage)
            self.__start_countdown(partial_countdown)

    def __render_countdown_stop_passage(self, passage):
        self.timer.stop()
        self.stats_view.hide_countdown()
        self.stats_view.show_image()

        if self.__show_body(passage):
            self.__show_alternatives(passage)

    def __start_countdown(self, partial_function):
        self.stats_view.hide_image()
        self.stats_view.show_countdown()

        self.stats_view.set_countdown("00:{}".format(self.count))
        self.count -= 1

        self.timer = QTimer()
        self.timer.timeout.connect(partial_function)
        self.timer.start(1000)

    # endregion


"""

    def __parse_exec_body_chunk(self, body_type, chunk):
        robot = self.experimental_utils.get_robot()

        for _, line in chunk.items():
            if body_type == BodyType.TEXT:
                if type(line) == StoryLine:
                    self.story_view.append_story_line(str(line) + "\n")

            elif body_type == BodyType.ROBOT:
                if type(line) == PoseMacro:
                    if robot is not None:
                        robot.pose(line.name)  # Blocking for a second

                if type(line) == SayMacro:
                    if robot is not None:
                        robot.say(line.sentence, line.emotion)  # Blocking for a second
                    self.story_view.append_story_line(str(line.sentence) + "\n")

                if type(line) == FeelMacro:
                    if robot is not None:
                        robot.feel(line.emotion)  # Blocking for a second

    def __show_body_in_chunks(self, passage=None):

        if self.interactive_body is not None:
            body_chunks = self.interactive_body
        else:
            self.story_view.set_btn_continue_txt("")
            body_chunks = passage.create_body_chunks()

        if len(body_chunks) == 0:
            self.interactive_body = None
            must_show_alternatives = True

        elif len(body_chunks) == 1:
            # Execute the last body chunk
            # set the interactive body to None

            _, (bt, chunk) = body_chunks.popitem()
            self.__parse_exec_body_chunk(bt, chunk)
            self.interactive_body = None
            must_show_alternatives = True

        else:
            _, (bt, chunk) = body_chunks.popitem()

            if bt == BodyType.TEXT:
                # it could be a TEXT or a FEEL
                # the next is going to be a ROBOT
                # So show the text and wait for an interaction
                # Before executing the robot chunk
                self.__parse_exec_body_chunk(bt, chunk)

                # Store the remaining of the body
                self.interactive_body = body_chunks

                # Wait for an user interaction
                self.story_view.set_continue_callback(self.__show_body_in_chunks)  # recursion
                self.story_view.set_btn_continue_txt("Continua")
                self.story_view.set_btn_continue_visible(True)
                self.story_view.hide_choice()
                must_show_alternatives = False

            else:
                # it could be a POSE and/or a SAY
                # The next is going to be a TEXT and/or a FEEL
                # So execute this blocking, but also show the next
                self.__parse_exec_body_chunk(bt, chunk)
                self.interactive_body = body_chunks
                must_show_alternatives = self.__show_body_in_chunks()  # recursion

        return must_show_alternatives

"""
