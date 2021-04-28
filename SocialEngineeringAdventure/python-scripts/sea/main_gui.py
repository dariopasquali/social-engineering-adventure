import sys

from sea.engine.seaEngine import SEAengine
from sea.experiment.ExperimentalUtils import ExperimentalUtils
from sea.view.gui.GUIView import GUIView

import yarp


class SeaParams:
    def __init__(self):
        self.module_name = ""
        self.source_file = ""

        self.random_seed = False
        self.seed = 42

        self.room_order = 1
        self.order_1 = [
            #'welcome', # Rules and Lore
            'intro',  # Meet with iCub
            #'R6',  # licenza smarrita
            #'SE0',  # ragno ghiaccio
            #'SER6',  # Dare la licenza ad iCub
            #'R2',  # Corridoio Buio
            #'SE6',  # Esposizione artefatti
            #'camp',  # Accampamento Dispersi
            #'SE4',  # Capslue
            #'lab',  # Laboratorio
            #'R0',  # Aiutare uomo in difficoltà
            #'SE5',  # Linux
            'SER4',  # Aiutare iCub
            #'SE2',  # Baratro
            #'SER0',  # Cerberus
            #'R4',  # Riposare all'aperto
            #'R3',  # Blob
            #'end'  # Ending
        ]
        self.order_2 = []
        self.dummy_order = [
            #'cross', 'trial', 'ending',
            #'welcome',
            #'testFlow',
            #'sbResources',
            #'sbCross',
            #'sbRoll',
            #'sbTrial',
            #'sbFight',
            #'sbItems',
            #'sbComplex',
            'TestEL',
            'TestGNI'
        ]

        self.debug_mode = False
        self.with_sound = False
        self.is_experiment = True
        self.do_wait_for_connections = False
        self.do_calibrate = False

        self.with_robot = True
        self.simulate_robot = False

        self.enable_mouse = True
        self.enable_gsr = True
        self.enable_eyelink = True
        self.enable_tobii = False

        self.eq_initial = None
        self.eq_low = None
        self.eq_medium = None
        self.eq_high = None

        self.language = "ita"

    def parse_room_order(self, rf, name, default):
        order = []

        room_bottle = rf.findGroup(name)
        for i in range(room_bottle.size()):
            room = room_bottle.get(i).asString()
            order.append(room)

        if len(order) == 0:
            order = default

        return order

    def parse_args(self):
        rf = yarp.ResourceFinder()
        rf.setVerbose(True)
        rf.setDefaultContext('sea')
        rf.setDefaultConfigFile('sea.ini')

        if not rf.configure(sys.argv):
            return False

        self.module_name = rf.check("name",
                                    yarp.Value("sea"),
                                    "module name (string)").asString()

        self.source_file = rf.check("source", yarp.Value("../../../Stories/smallest_sea.html"),
                                    "source file of the story (string)").asString()

        # GUI CONTROL
        lang_raw = rf.check("lang", yarp.Value("ita"), "ita or eng").asString()
        if lang_raw in ['eng', 'ENG', 'EN', 'en', 'english']:
            self.language = "eng"
        else:
            self.language = "ita"

        # Experiment Stuff
        self.is_experiment = rf.check("experiment", yarp.Value(True),
                                      "Flag to turn on the experimental utils (yarp, sensors, robot)").asBool()

        self.do_wait_for_connections = rf.check("wait_for_connections", yarp.Value(False),
                                                "Wait for the connections before starting").asBool()

        self.do_calibrate = rf.check("calibrate", yarp.Value(False),
                                                "Calibrate the sensors before starting").asBool()

        # Random control
        self.random_seed = rf.check("random_seed", yarp.Value(False),
                                    "Flag to use a random seed for dice rolls").asBool()
        self.seed = rf.check("seed", yarp.Value(42), "The random seed for dice rolls").asInt()

        # FLAGS
        self.debug_mode = rf.check("debug", "Flag to turn on the dummy order of rooms")
        self.with_sound = rf.check("sound", "Flag to turn on the sound effects")

        # ROBOT
        self.with_robot = rf.check("robot", yarp.Value(True), "Enables the robot control").asBool()
        self.simulate_robot = rf.check("simulate_robot", yarp.Value(False), "If true, spawn a simulated Robot").asBool()

        # SENSORS
        self.enable_mouse = rf.findGroup("DEVICES").check("mouse", yarp.Value(True),
                                                          "Enable the mouse interface (bool)").asBool()
        self.enable_gsr = rf.findGroup("DEVICES").check("gsr", yarp.Value(True),
                                                        "Enable the Shimmer3 GSR+ interface (bool)").asBool()
        self.enable_eyelink = rf.findGroup("DEVICES").check("eyelink", yarp.Value(True),
                                                            "Enable the Eyelink 1000 interface (bool)").asBool()
        self.enable_tobii = rf.findGroup("DEVICES").check("tobii", yarp.Value(False),
                                                          "Enable the Tobii Pro interface (bool)").asBool()

        # ROOM_ORDER
        self.room_order = rf.check("room_order", yarp.Value(0), "0 = dummy, 1 = order 1, 2 = order 2").asInt()
        self.order_1 = self.parse_room_order(rf, "order_1", self.order_1)
        self.order_2 = self.parse_room_order(rf, "order_2", self.order_2)
        self.dummy_order = self.parse_room_order(rf, "dummy_order", self.dummy_order)

        # QUANTUM ENERGY
        self.eq_initial = rf.findGroup("EQ").check("initial", yarp.Value(50), "Initial Quantum Energy Value").asInt()
        self.eq_low = rf.findGroup("EQ").check("low", yarp.Value(5), "Normal EQ gain/loss").asInt()
        self.eq_medium = rf.findGroup("EQ").check("medium", yarp.Value(10),
                                                  "Medium EQ gain/loss, for dumb decisions you can avoid").asInt()
        self.eq_high = rf.findGroup("EQ").check("high", yarp.Value(20),
                                                "high EQ gain/loss, great prizes come at great cost!").asInt()



        return True

    def get_order(self):
        if self.debug_mode or self.room_order == 0:
            return self.dummy_order

        if self.room_order == 1:
            return self.order_1

        if self.room_order == 2:
            return self.order_2

    def get_name(self):
        return "/{}".format(self.module_name)

    def get_sensors(self):
        return {
            "mouse": self.enable_mouse,
            "gsr": self.enable_gsr,
            "eyelink": self.enable_eyelink,
            "tobii": self.enable_tobii
        }

    def log_params(self, logger):
        logger("source = {}".format(self.source_file))
        logger("room_order = {}".format(self.room_order))
        logger("is_experiment = {}".format(self.is_experiment))
        logger("with_robot = {}".format(self.with_robot))
        logger("with_sound = {}".format(self.with_sound))
        logger("language = {}".format(self.language))


def init_sea_engine(params):
    engine = SEAengine()
    engine.load_dungeon(filename=params.source_file, room_order=params.get_order())
    engine.init_environment(eq_initial=params.eq_initial, eq_low=params.eq_low,
                            eq_medium=params.eq_medium, eq_high=params.eq_high,
                            random_seed=params.random_seed, seed=params.seed,
                            lang=params.language)
    return engine


def main(params):
    # Init the Game
    sea_engine = init_sea_engine(params)
    sea_engine.start_game()

    # Init the Sensing and YARP utils (Blocking)
    experiment = ExperimentalUtils(root_name=params.get_name(),
                                   with_yarp=params.is_experiment,
                                   with_robot=params.with_robot,
                                   sensor_flags=params.get_sensors(),
                                   do_wait_for_connection=params.do_wait_for_connections)

    # Init the GUIView
    sea_gui = GUIView(sea_engine, experiment, monitor_id=1, with_sound=params.with_sound, lang=params.language)
    app = sea_gui.init_gui_engine()

    # Check everything is loaded
    if app is None:
        print("ERROR! LOADING THE GUI")
        sys.exit(1)

    # Log the parameters
    params.log_params(experiment.log)

    # Calibrate the devices which needs it (Blocking)
    if params.do_calibrate:
        experiment.calibrate()

    # Start the experiment and streaming devices
    experiment.start_experiment()

    # Run the GUI app as a Daemon
    sys.exit(app.exec_())


if __name__ == "__main__":

    # Load the params with the yarp ResourceFinder
    params = SeaParams()
    ok = params.parse_args()

    if not ok:
        print("Error loading the parameters!")
        exit(1)

    # Start the program
    main(params)
