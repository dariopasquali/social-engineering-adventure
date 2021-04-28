import yarp
import time


class DummyRobot(yarp.BottleCallback):

    def onRead(self, *args):
        print("Received Cmd {}".format(args[0].toString()))
        for i in range(5):
            print("."*(i+1))
            time.sleep(0.5)
        print("End Cmd")

        btl = self.ack.prepare()
        btl.clear()
        btl.addString("ack")
        self.ack.write()

    def __init__(self):
        super().__init__()
        yarp.Network_init()

        self.input = yarp.BufferedPortBottle()
        self.ack = yarp.BufferedPortBottle()

        self.input.useCallback(self)

        self.input.open("/cmd:i")
        self.ack.open("/ack:o")

        yarp.Network.connect("/sea/puppet/async/cmd:o", "/cmd:i")
        yarp.Network.connect("/ack:o", "/sea/puppet/async/ack:i")

        self.run = True

    def close(self):
        self.run = False
        self.input.interrupt()
        self.ack.interrupt()

        self.input.close()
        self.ack.close()

    def start(self):
        while self.run:
            pass

        print("Closing")


if __name__ == "__main__":
    robot = DummyRobot()
    robot.start()
