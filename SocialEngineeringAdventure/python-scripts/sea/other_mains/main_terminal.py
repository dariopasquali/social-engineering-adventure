from sea.engine.model.Passage import PassageType
from sea.engine.seaEngine import SEAengine
from sea.experiment.ExperimentalUtils import ExperimentalUtils
from sea.view.terminal.Terminal import *


def main():
    filename = "./smallest_sea.html"
    order = ['R6', 'SE0', 'SER6', 'R2', 'SE6', 'camp',
             'SE4', 'lab', 'R0', 'SE5', 'SER4', 'SE2', 'SER0',
             'R4', 'R3', 'end']

    dummy_order = [
        'sbCross',
        #'sbFight',
        #'sbResources',
        #'sbTrial',
        #'sbRoll',
        #'sbItems'
    ]

    # Init Game
    engine = SEAengine()
    engine.init_environment()
    engine.load_dungeon(filename, dummy_order)
    engine.start_game()

    experiment = ExperimentalUtils()

    # Init Terminal interface
    terminal = TerminalView(experiment)

    while engine.is_running and engine.is_alive():

        # Clear the view
        terminal.clear()

        # Load room and passage
        passage = engine.current_passage

        # Exec the correct rendering function based on the passage type
        terminal.render_current_passage(engine, passage)


if __name__ == '__main__':
    main()




