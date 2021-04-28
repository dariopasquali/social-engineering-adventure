"""
Methods to play the story via terminal
"""
import os

from sea.engine.model.Passage import PassageType


class TerminalView:

    def __init__(self, experimental_utils):

        self.experimental_utils = experimental_utils

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
        PassageType.EXEC: self.__render_text_passage,
        #PassageType.COUNTDOWN: self.__render_text_passage,
    }

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_current_passage(self, engine, passage):
        return self.__rendering_map[passage.passage_type](engine, passage)

    def __read_input(self, options):
        print('?? ', end='')
        ans = input()

        #print("{} in {}".format(ans, options))
        while ans == '' or ans == '1000' or int(ans) not in options:
            ans = input()

        return int(ans)

    def __show_body(self, passage):
        print("===========================================")
        # Show the body
        for _, line in passage.body_lines.items():
            if not line.is_empty():
                print(line)

        print("")

    def __show_alternatives_read_choice(self, passage):
        alternatives = []
        # Show the alternatives
        for id, link in passage.links.items():
            alternatives.append(int(id))
            print("{} -> {}".format(id, link.text))

        return self.__read_input(alternatives)

    def __render_text_passage(self, engine, passage):

        self.__show_body(passage)
        choice = self.__show_alternatives_read_choice(passage)

        if choice == 1000:
            # Skip room
            engine.next_room()
        else:
            # Update state
            next_p = passage.links[choice].toPassage
            engine.next_passage(next_p)

    def __render_endpoint_passage(self, engine, passage):
        # Just show the next room
        engine.next_room()

    def __render_back_passage(self, engine, passage):
        if not engine.go_back():
            # if I CANNOT go back, just present again the choice
            print("Purtroppo hai esplorato tutte le strade alternative")
            print("Prosegui! puoi farcela")
        else:
            # if I can go back, the room and passage has been updated
            self.__show_body(passage)

        print("INVIO -> Continua")
        input()

    def __render_backtrack_passage(self, engine, passage):
        self.__show_body(passage)
        print("INVIO -> Continua")
        input()
        engine.next_room()

    def __render_fight_passage(self, engine, passage):
        self.__show_body(passage)
        print("INVIO -> Lancia il dado")
        input()

        print("roll...")
        check_result, dice_result = engine.roll_attack_and_check()
        print("Hai fatto {}!".format(dice_result))
        print("INVIO -> Continua")
        input()

        # Update state
        if check_result:
            # Success
            next_p = passage.links[0].toPassage
        else:
            # File
            next_p = passage.links[1].toPassage

        engine.next_passage(next_p)

    def __render_roll_passage(self, engine, passage):
        self.__show_body(passage)
        print("INVIO -> Lancia il dado")
        input()

        print("roll...")
        check_result, dice_result = engine.roll_dice_and_check()
        print("Hai fatto {}!".format(dice_result))
        print("INVIO -> Continua")
        input()

        # Update state
        if check_result:
            # Success
            next_p = passage.links[0].toPassage
        else:
            # File
            next_p = passage.links[1].toPassage

        engine.next_passage(next_p)

    def __render_trial_passage(self, engine, passage):
        print("Render Trial")

        self.__show_body(passage)
        print("--------------- START {} {} {}".format(passage.trial_type, passage.trial_id, passage.trial_seq))
        choice = self.__show_alternatives_read_choice(passage)
        print("--------------- STOP {} {} {} | {}".format(passage.trial_type, passage.trial_id, passage.trial_seq, choice))

        input()
        if choice == 1000:
            # Skip room
            engine.next_room()
        else:
            # Update state
            next_p = passage.links[choice].toPassage
            engine.next_passage(next_p)

    def __render_item_check_passage(self, engine, passage):
        self.__show_body(passage)

        print(">>> Inventory <<<")
        for item in engine.get_inventory().items():
            print(str(item[1]))
        print("-----------------")

        check_result = engine.check_have_item()
        print("INVIO -> Continua")
        input()

        # Update state
        if check_result:
            # Success
            next_p = passage.links[0].toPassage
        else:
            # File
            next_p = passage.links[1].toPassage

        engine.next_passage(next_p)

    def __render_end_passage(self, engine, passage):
        self.__show_body(passage)
        engine.end_game()
