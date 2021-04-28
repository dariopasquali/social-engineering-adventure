from sea.experiment.devices.DeviceInterface import DeviceInterface, DeviceMode
import yarp

VOCAB_START = yarp.createVocab('s', 't', 'a', 'r')
VOCAB_STOP = yarp.createVocab('s', 't', 'o', 'p')
VOCAB_ANNOTATE = yarp.createVocab('a', 'n', 'n', 't')

VOCAB_TRIAL = yarp.createVocab('t', 'r', 'l')
VOCAB_ANNOTATION = yarp.createVocab('a', 'n', 'n', 't')
VOCAB_EXPERIMENT = yarp.createVocab('e', 'x', 'p', 0)
VOCAB_MODE = yarp.createVocab('m', 'o', 'd', 'e')

VOCAB_CALIBRATE = yarp.createVocab('c', 'a', 'l', 'i')
VOCAB_STORE = yarp.createVocab('s', 't', 'o', 'r')


class EyeLinkInterface(DeviceInterface):

    def __init__(self, port_name):
        super().__init__(port_name, DeviceMode.RPC)

    # Start and Stop Trial not required

    def start_experiment(self):
        cmd = yarp.Bottle()

        # Set the Annotation Mode
        cmd.clear()
        cmd.addVocab(VOCAB_MODE)
        cmd.addVocab(VOCAB_ANNOTATION)
        self.rpc_write(cmd)

        cmd.clear()
        cmd.addVocab(VOCAB_EXPERIMENT)
        cmd.addVocab(VOCAB_START)
        self.rpc_write(cmd)

    def stop_experiment(self):
        cmd = yarp.Bottle()

        # Stop the experiment
        cmd.clear()
        cmd.addVocab(VOCAB_EXPERIMENT)
        cmd.addVocab(VOCAB_START)
        self.rpc_write(cmd)

        # Store the data
        cmd.clear()
        cmd.addVocab(VOCAB_STORE)
        self.rpc_write(cmd)

    def calibrate(self):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_CALIBRATE)
        self.rpc_write(cmd)

    def annotate(self, annotation):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_ANNOTATE)
        cmd.addString(annotation)
        self.rpc_write(cmd)

    # Back plan usable in annotation mode
    def start_trial(self, trial_type, trial_id, trial_seq):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_TRIAL)
        cmd.addString(trial_type)
        cmd.addString(trial_id)
        cmd.addString(trial_seq)
        self.rpc_write(cmd)

    def stop_trial(self, trial_type, trial_id, trial_seq, decision=None):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_TRIAL)
        cmd.addString(trial_type)
        cmd.addString(trial_id)
        cmd.addString(trial_seq)
        cmd.addInt(decision)
        self.rpc_write(cmd)
