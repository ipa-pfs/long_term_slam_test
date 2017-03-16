#!/usr/bin/python
import unittest
import rospy
import rostest
import roslib
import roslaunch
import tf
import math
import sys
import rospkg
from rosgraph_msgs.msg import Log
from atf_core import ATF
from simple_script_server import *
from ipa_map_comparison.srv import *

from atf_core import ATF

class Application:
    def __init__(self):
        # initialize the ATF class
        self.atf = ATF() 
        #rospy.Subscriber("/rosout_agg", Log, self.state_transition_cb, queue_size=None)

    def state_transition_cb(self, msg):
        # TODO sm feedback on state change [eg: ERROR, READY, BUSY ...] 
        rospy.loginfo("callback")
        if 'Done.' in msg.msg:
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
        name = rospy.get_param('atf/robot_config/additional_arguments/file_name')
        ndt_mapping = str(rospy.get_param('atf/robot_config/additional_arguments/ndt_mapping'))
        resolution = str(rospy.get_param('atf/robot_config/additional_arguments/int_res'))
        ndt_str=''
        if ndt_mapping == 1:
            ndt_str = 'ndt'
        else:
            ndt_str = 'no_ndt'
        observation_model = str(rospy.get_param('atf/robot_config/additional_arguments/observation_model'))
        number_of_neighbours =(rospy.get_param('atf/robot_config/additional_arguments/number_of_neighbours'))
        neighbourhood_score = (rospy.get_param('atf/robot_config/additional_arguments/number_of_neighbours'))
        eval_file_name = "eval_" + str(observation_model) + "_" + str(resolution) + "_" + ndt_str + "_" + str(number_of_neighbours) +"_"+str(neighbourhood_score) +".txt"
        map_file_name = "map_" + str(observation_model) + "_" + str(resolution) + "_" + ndt_str + "_" + str(number_of_neighbours) +"_"+str(neighbourhood_score)
        # #place = str(name).find('file_name') + str(name).find()
        # #end = 
        map_path='asd'
        rospack = rospkg.RosPack()
        rospack.list()
        map_path = rospack.get_path('ipa_map_comparison')
        map_path = map_path +'/maps/'
        rospy.logerr(str(map_path))
        #rospy.logerr(str(name['atf']['robot_config']['additional_arguments']['file_name']))
        rospy.sleep(550)
        # Do something else
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/srd-ps/git/ipa_navigation_catkin/src/evaluation_tools/ipa_map_comparison/launch/map_saver.launch"])

        launch.start()
        rospy.sleep(5)
        launch.shutdown()

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/srd-ps/git/ipa_navigation_catkin/src/evaluation_tools/ipa_map_comparison/launch/map_comparision_node.launch"])
        launch.start()
        rospy.sleep(5)
        launch.shutdown()
        start_map_eval = rospy.ServiceProxy('/startMapEval', StartMapEval)
        start_map_eval(eval_file_name, number_of_neighbours, neighbourhood_score)
        new_map_path = map_path "map"+"_"+ str(observation_model) + "_" + ndt_str +"/" +map_file_name
        map_path = map_path + "map"
        shutil.move(map_path + ".pgm", new_map_path +".pgm")
        shutil.move(map_path + ".yaml", new_map_path +".yaml")

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

