from sea.experiment.devices.DeviceInterface import DeviceInterface, DeviceMode
import yarp

VOCAB_START = yarp.createVocab('s', 't', 'a', 'r')
VOCAB_STOP = yarp.createVocab('s', 't', 'o', 'p')


class MouseInterface(DeviceInterface):

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
