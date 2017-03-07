#!/usr/bin/python
import unittest
import rospy
import rostest
import tf
import math
import sys

from atf_core import ATF
from simple_script_server import *

from atf_core import ATF

class Application:
    #rospy.Subscriber("/rosout_agg", Log, self.state_transition_cb, queue_size=None)
    def __init__(self):
        # initialize the ATF class
        self.atf = ATF() 

    def state_transition_cb(self, msg):
        # TODO sm feedback on state change [eg: ERROR, READY, BUSY ...] 
        if 'subscribed to person_of_interest_filter' in msg.msg:
            self.ready_for_scenario = True

    def execute(self):
        # you can call start/pause/purge/stop for each testblock during the execution of your app
        rospy.sleep(5)
        #self.atf.start("testblock_all")
        self.atf.start("testblock_small")
        # Do something
        #self.wait_for_robot_ready();
        #self.atf.stop("testblock_1")
        #self.atf.start("testblock_2")

        # Do something else
        rospy.sleep(200)
        self.atf.stop("testblock_small")
        #self.atf.stop("testblock_all")

        # finally we'll have to call shutdown() to tell the ATF to stop all recordings and wrap up
        self.atf.shutdown()

    def wait_for_robot_ready(self):
        rospy.loginfo("wait for robot to be ready")
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            if self.ready_for_scenario:
                break
            r.sleep()
class Test(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        pass

    def test_Recording(self):
        self.app.execute()

if __name__ == '__main__':
    rospy.init_node('test_name')
    rostest.rosrun('application', 'recording', Test, sysargs=None)

