from sea.experiment.devices.DeviceInterface import DeviceInterface, DeviceMode
import yarp


VOCAB_START = yarp.createVocab('S', 'T', 'A', 'R')
VOCAB_STOP = yarp.createVocab('S', 'T', 'O', 'P')


class GSRInterface(DeviceInterface):

    def __init__(self, port_name):
        super().__init__(port_name, DeviceMode.RPC)

    # Start and Stop Trial not required

    def start_experiment(self):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_START)
        self.rpc_write(cmd)

    def stop_experiment(self):
        cmd = yarp.Bottle()
        cmd.clear()
        cmd.addVocab(VOCAB_STOP)
        self.rpc_write(cmd)
