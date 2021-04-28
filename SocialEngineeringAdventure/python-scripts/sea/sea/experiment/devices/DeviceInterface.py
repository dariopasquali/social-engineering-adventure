from enum import Enum

import yarp

"""
Class to interact with a YARP device
we have two types of device

- Devices you just start and stop (Mouse, GSR, Tobii Streaming)
    - You dump the whole stream along with the annotations
    - Then segment the stream based on the annotations
    
- Devices which internally keep track of the trials (Eyelink, Tobii Events)
    - You start / stop the device
    - And trigger the begin and end of each trial
    - Dumping also the annotations
    - Then pair the begin and ends of trials and annotations
"""

class DeviceMode(Enum):
    RPC = 0,
    WRITE = 1,
    BOTH = 2
    NONE = 3


class DeviceInterface:
    def __init__(self, root_name, mode=DeviceMode.NONE):

        self.device_name = root_name
        self.mode = mode

        if mode == DeviceMode.NONE:
            return

        if mode in [DeviceMode.BOTH, DeviceMode.RPC]:
            self.rpc_port = yarp.RpcClient()
            self.rpc_port.open(root_name + "/rpc")
        elif mode in [DeviceMode.BOTH, DeviceMode.WRITE]:
            self.write_out = yarp.BufferedPortBottle()
            self.write_in = yarp.BufferedPortBottle()

            self.write_out.open(root_name + "/cmd:o")
            self.write_in.open(root_name + "/ack:i")

    # Write a Bottle to the port
    def rpc_write(self, cmd):
        resp_bottle = yarp.Bottle()
        resp_bottle.clear()
        self.rpc_port.write(cmd, resp_bottle)

        return resp_bottle.get(0).asString()

    def write(self, cmd):
        cmd_bottle = self.write_out.prepare()
        for i in range(cmd.size()):
            cmd_bottle.add(yarp.Value(cmd.get(i)))

        self.write_out.write()

    def wait_for_connections(self):

        if self.mode == DeviceMode.NONE:
            return

        if self.mode in [DeviceMode.BOTH, DeviceMode.RPC]:
            print("Wait for the rpc port")
            while self.rpc_port.getOutputCount() < 1:
                pass

        elif self.mode in [DeviceMode.BOTH, DeviceMode.WRITE]:
            print("Wait for the output write port")
            while self.write_out.getOutputCount() < 1:
                pass

            print("Wait for the input write port")
            while self.write_in.getInputCount() < 1:
                pass

    def calibrate(self):
        pass

    def annotate(self, annotation_params):
        pass

    def start_experiment(self):
        pass

    def stop_experiment(self):
        pass

    def start_trial(self, trial_type, trial_id, trial_seq):
        pass

    def stop_trial(self, trial_type, trial_id, trial_seq, decision=None):
        pass
