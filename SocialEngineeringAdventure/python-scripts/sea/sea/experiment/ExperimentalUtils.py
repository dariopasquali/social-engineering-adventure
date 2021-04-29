"""
Interface class to control sensors like
- shimmer
- tobii
- eyelink
- mouse
"""
from sea.experiment.RobotInterface import RobotInterface
from sea.experiment.YARPInterface import YARPInterface
from sea.experiment.devices.EyeLinkInterface import EyeLinkInterface
from sea.experiment.devices.GSRInterface import GSRInterface
from sea.experiment.devices.MouseInterface import MouseInterface
from sea.experiment.devices.TobiiEventInterface import TobiiEventInterface
from sea.experiment.devices.TobiiStreamingInterface import TobiiStreamingInterface
from sea.experiment.experimental_enums import LogLevel


class ExperimentalUtils:
    def __init__(self, root_name="/sea", with_yarp=False, with_robot=False, sensor_flags={},
                 do_wait_for_connection=False):

        self.devices = []
        self.with_yarp = with_yarp
        self.with_robot = with_robot

        if with_yarp:

            self.yarp_interface = YARPInterface(root_name=root_name, port_name="not_used")

            self.log_by_level = {
                LogLevel.INFO: self.yarp_interface.log_info,
                LogLevel.DEBUG: self.yarp_interface.log_debug,
                LogLevel.ERROR: self.yarp_interface.log_error,
            }

            if self.with_robot:
                self.robot_interface = RobotInterface(root_name)
                if do_wait_for_connection:
                    self.robot_interface.wait_for_connections()


            self.__init_sensors(root_name, sensor_flags)
            if do_wait_for_connection:
                self.wait_for_connections()

        else:
            print("Skip YARP init!")

    def get_robot(self):
        if self.with_robot:
            return self.robot_interface
        return None

    # Log on YARP
    def log(self, message, level=LogLevel.INFO):
        if self.with_yarp:
            self.log_by_level[level](message)
        else:
            print(message)

    # Spawn the sensors defined in the YARP config
    def __init_sensors(self, root_name, flags):
        self.devices.append(self.yarp_interface)

        if flags["mouse"]:
            self.log("Start Mouse Interface!")
            self.devices.append(MouseInterface(root_name + "/mouse"))

        if flags['eyelink']:
            self.log("Start GSR Interface!")
            self.devices.append(EyeLinkInterface(root_name + "/eyelink"))

        if flags['gsr']:
            self.log("Start Eyelink Interface!")
            self.devices.append(GSRInterface(root_name + "/gsr"))

        if flags['tobii']:
            self.log("Start Tobii Interface!")
            self.devices.append(TobiiEventInterface(root_name + "/tobii/events/rpc"))
            # self.devices.append(TobiiStreamingInterface(root_name + "/tobii/events/rpc"))

    def wait_for_connections(self):
        # Blocking
        for device in self.devices:
            self.log("Wait for the connections of {}".format(device.device_name))
            print("Wait for the connections of {}".format(device.device_name))
            device.wait_for_connections()

    def calibrate(self):
        for device in self.devices:
            self.log("Calibrate {}".format(device.device_name))
            device.calibrate()

    def start_experiment(self):
        print("EXPERIMENT START")

        if not self.with_yarp:
            return
        self.log("EXPERIMENT START")
        for dev in self.devices:
            dev.start_experiment()

    def end_experiment(self):
        print("EXPERIMENT END")

        if not self.with_yarp:
            return
        self.log("EXPERIMENT END")
        for dev in self.devices:
            dev.stop_experiment()

    """
    ANNOTATION SEQUENCE:
    
    ROOM START <name>
    
    PASSAGE START <name> <type> <eq> <power>
    [TRIAL <type> <id> <seq>]
    RENDERING START
    RENDERING END
    CONTINUE
    -> PASSAGE END
    -> DECISION R/L/C -> PASSAGE END
    
    ...
    
    ROOM END
    """

    def annotate(self, annotation_params):
        params = [str(p) for p in annotation_params]
        annotation = " ".join(params)
        self.log(annotation)
        for dev in self.devices:
            dev.annotate(annotation)

    # def annotate(self, passage_name, event, hp=0, power=0, trial_type="", trial_id="", trial_seq="", decision=""):
    #     params = "{} {} {} {} {} {} {} {}".format(event, passage_name, hp, power, decision, trial_type, trial_id, trial_seq)
    #     self.log("{}".format(params))
    #     print("{}".format(params))
    #     for dev in self.devices:
    #         dev.annotate(params)