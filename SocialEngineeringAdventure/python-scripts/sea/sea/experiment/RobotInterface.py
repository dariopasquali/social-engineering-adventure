import yarp

LOG_INFO = yarp.createVocab('I', 'N', 'F', 'O')
LOG_DEBUG = yarp.createVocab('D', 'B', 'G', 0)
LOG_ERROR = yarp.createVocab('E', 'R', 'R', 0)

CMD_SAY = yarp.createVocab('s', 'a', 'y', 0)
CMD_POSE = yarp.createVocab('p', 'o', 's', 'e')
CMD_FEEL = yarp.createVocab('f', 'e', 'e', 'l')


class AckProcessor(yarp.BottleCallback):

    def __init__(self):
        super().__init__()
        self.callback = None

    def set_ack_callback(self, callback):
        #print("set the callback")
        self.callback = callback

    def onRead(self, *args):
        #print("onRead")
        if self.callback is not None:
            #print("CALLBACK!!")
            self.callback()
            #self.callback = None


class RobotInterface:

    def __init__(self, root_name="experiment"):
        print("Init YARP")
        yarp.Network.init()

        # YARP ports
        self.outport_puppets_rpc = yarp.RpcClient()

        self.output_async_cmd = yarp.BufferedPortBottle()
        self.input_async_ack = yarp.BufferedPortBottle()

        # I don't really know if this works
        self.ack_processor = AckProcessor()
        self.input_async_ack.useCallback(self.ack_processor)

        # Open Ports
        self.outport_puppets_rpc.open(root_name + "/puppet/rpc")

        self.output_async_cmd.open(root_name + "/puppet/async/cmd:o")
        self.input_async_ack.open(root_name + "/puppet/async/ack:i")

    def set_ack_port_callback(self, callback):
        self.ack_processor.set_ack_callback(callback)

    def wait_for_connections(self):
        print("Wait for the async commands")
        while self.output_async_cmd.getOutputCount() < 1:
            pass

        print("Wait for the acks")
        while self.input_async_ack.getInputCount() < 1:
            pass

    def close(self):
        self.outport_puppets_rpc.interrupt()
        self.output_async_cmd.interrupt()
        self.input_async_ack.interrupt()

        self.outport_puppets_rpc.close()
        self.output_async_cmd.close()
        self.input_async_ack.close()

    # blocking
    def say(self, sentence, emotion=""):
        cmd_bottle = yarp.Bottle()
        reply_bottle = yarp.Bottle()

        cmd_bottle.clear()
        reply_bottle.clear()

        cmd_bottle.addVocab(CMD_SAY)
        cmd_bottle.addString(sentence)
        if emotion != "":
            cmd_bottle.addString(emotion)
        self.outport_puppets_rpc.write(cmd_bottle, reply_bottle)
        print(reply_bottle.get(0).asString())
        return reply_bottle.get(0).asString() == "ack"

    # Not Blocking
    def say_async(self, sentence, emotion=""):
        cmd_bottle = self.output_async_cmd.prepare()
        cmd_bottle.clear()
        cmd_bottle.addVocab(CMD_SAY)
        cmd_bottle.addString(sentence)
        if emotion != "":
            cmd_bottle.addString(emotion)

        self.set_ack_port_callback(None)
        self.output_async_cmd.write()

    # blocking
    def feel(self, emotion):
        cmd_bottle = yarp.Bottle()
        reply_bottle = yarp.Bottle()

        cmd_bottle.clear()
        reply_bottle.clear()

        cmd_bottle.addVocab(CMD_FEEL)
        cmd_bottle.addString(emotion)
        self.outport_puppets_rpc.write(cmd_bottle, reply_bottle)
        return reply_bottle.get(0).asString() == "ack"

    # Not Blocking
    def feel_async(self, emotion):
        cmd_bottle = self.output_async_cmd.prepare()
        cmd_bottle.clear()
        cmd_bottle.addVocab(CMD_FEEL)
        cmd_bottle.addString(emotion)

        self.set_ack_port_callback(None)
        self.output_async_cmd.write()

    # blocking
    def pose(self, poseName):
        cmd_bottle = yarp.Bottle()
        reply_bottle = yarp.Bottle()

        cmd_bottle.clear()
        reply_bottle.clear()

        cmd_bottle.addVocab(CMD_POSE)
        cmd_bottle.addString(poseName)
        self.outport_puppets_rpc.write(cmd_bottle, reply_bottle)
        return reply_bottle.get(0).asString() == "ack"

    # Not Blocking
    def pose_async(self, poseName):
        cmd_bottle = self.output_async_cmd.prepare()
        cmd_bottle.clear()
        cmd_bottle.addVocab(CMD_POSE)
        cmd_bottle.addString(poseName)

        self.set_ack_port_callback(None)
        self.output_async_cmd.write()
