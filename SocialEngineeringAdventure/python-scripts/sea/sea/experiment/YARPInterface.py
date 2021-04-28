"""
Interface class to access yarp logging and annotation functionalities
"""
import yarp

from sea.experiment.devices.DeviceInterface import DeviceInterface, DeviceMode

LOG_INFO = yarp.createVocab('I', 'N', 'F', 'O')
LOG_DEBUG = yarp.createVocab('D', 'B', 'G', 0)
LOG_ERROR = yarp.createVocab('E', 'R', 'R', 0)

EXEC = yarp.createVocab('e', 'x', 'e', 'c')
TRIAL = yarp.createVocab('T', 'R', 'L', 0)


class YARPInterface(DeviceInterface):

    def __init__(self, port_name="", root_name="experiment"):
        super().__init__(port_name, mode=DeviceMode.NONE)
        print("Init YARP")
        yarp.Network.init()

        # YARP ports
        # root
        self.outport_logging = yarp.BufferedPortBottle()
        self.outport_annotations = yarp.BufferedPortBottle()

        # Open Ports
        self.outport_logging.open(root_name + "/log:o")
        self.outport_annotations.open(root_name + "/annotations:o")

    def wait_for_connections(self):
        print("Wait for the logging port")
        while self.outport_logging.getOutputCount() < 1:
            pass

        print("Wait for the annotation port")
        while self.outport_annotations.getOutputCount() < 1:
            pass

    def log_info(self, message):
        bottle = self.outport_logging.prepare()
        bottle.clear()
        bottle.addVocab(LOG_INFO)
        bottle.addString(message)
        self.outport_logging.writeStrict()

    def log_debug(self, message):
        bottle = self.outport_logging.prepare()
        bottle.clear()
        bottle.addVocab(LOG_DEBUG)
        bottle.addString(message)
        self.outport_logging.writeStrict()

    def log_error(self, message):
        bottle = self.outport_logging.prepare()
        bottle.clear()
        bottle.addVocab(LOG_ERROR)
        bottle.addString(message)
        self.outport_logging.writeStrict()

    def close(self):
        self.outport_logging.interrupt()
        self.outport_annotations.interrupt()
        self.outport_logging.close()
        self.outport_annotations.close()

    def start_experiment(self):
        bottle = self.outport_annotations.prepare()
        bottle.clear()
        bottle.addString("START EXPERIMENT")
        self.outport_annotations.writeStrict()

    def stop_experiment(self):
        bottle = self.outport_annotations.prepare()
        bottle.clear()
        bottle.addString("STOP EXPERIMENT")
        self.outport_annotations.writeStrict()

    def annotate(self, annotation):
        bottle = self.outport_annotations.prepare()
        bottle.clear()
        bottle.addString(annotation)
        self.outport_annotations.writeStrict()

    # def annotate_trial_start(self, trial_type, trial_id, trial_seq):
    #     bottle = self.outport_annotations.prepare()
    #     bottle.clear()
    #     bottle.addVocab(TRIAL)
    #     bottle.addString(trial_type)
    #     bottle.addString(trial_id)
    #     bottle.addString(trial_seq)
    #     self.outport_annotations.write()
    #
    # def annotate_trial_stop(self, trial_type, trial_id, trial_seq, choice):
    #     bottle = self.outport_annotations.prepare()
    #     bottle.clear()
    #     bottle.addVocab(TRIAL)
    #     bottle.addString(trial_type)
    #     bottle.addString(trial_id)
    #     bottle.addString(trial_seq)
    #     bottle.addInt(choice)
    #     self.outport_annotations.write()
