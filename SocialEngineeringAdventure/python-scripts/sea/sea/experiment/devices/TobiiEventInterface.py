from sea.experiment.devices.DeviceInterface import DeviceInterface, DeviceMode
import yarp

VOCAB_EVENT = yarp.createVocab('E', 'V', 'T', 0)


class TobiiEventInterface(DeviceInterface):

    def __init__(self, port_name):
        super().__init__(port_name, DeviceMode.RPC)

    # Start and Stop Trial not required

    def start_trial(self, trial_type, trial_id, trial_seq):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_EVENT)
        cmd.addString(trial_type)
        cmd.addInt(trial_id)
        cmd.addInt(trial_seq)
        self.rpc_write(cmd)

    def stop_trial(self, trial_type, trial_id, trial_seq, decision=None):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_EVENT)
        cmd.addString(trial_type)
        cmd.addInt(trial_id)
        cmd.addInt(trial_seq)
        cmd.addString(decision)
        self.rpc_write(cmd)
