#!/usr/bin/env python

import rospy
import tf
import math
import yaml

import os.path

#file_path = '/home/fmw-hb/atf_catkin_ws/src/atf/hannes_test/config/robots'
class robot_maker():
    def __init__(self):
        self.int_res = [0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
        self.ndt_mapping = [True, False]
        self.ndt_matching = [False]
        self.observation_model = ["gaussianRange","standard"]
        self.standard_deviation_range = [0.02]
        self.file_path = '/home/srd-ps/git/test_ws/src/long_term_slam_test/config/robots/'
        self.robots = ""


    def make_robots(self):
        for n in range(0, 2):
            for obs in self.observation_model:
                for ndt in self.ndt_mapping:
                    for res in self.int_res:
                        for matching in self.ndt_matching:
                            for dev in self.standard_deviation_range:
                                if (ndt == False and matching == True):
                                    continue
                                if (ndt == True):
                                    ndt_str ="ndt_mapping"
                                else:
                                    ndt_str="no_ndt_mapping"
                                if (matching ==True):
                                    ndt_match_str ="ndt_matching"
                                else:
                                    ndt_match_str="no_ndt_matching"
                                filename = str(obs)+"_"+str(res)+"m_"+ndt_str+"_"+str(ndt_match_str)+"_"+str(dev)+"_"+str(n)
                                # save everything in the file
                                #with open(self.file_path+filename, 'w') as stream:
                                print "Path: "+self.file_path+filename
                                robot = open(self.file_path+filename+".yaml", 'w')
                                robot.write("robot_bringup_launch: \"launch/all.launch\"\nwait_for_topics: []\nwait_for_services: []\n"
                                             "additional_parameters:\n  \"/use_sim_time\": true\n"
                                             "additional_arguments:\n  \"int_res\": "+str(res)+"\n  \"standard_deviation_range\": "+str(dev)+
                                             "\n  \"static_map\": true\n  \"ndt_mapping\": " +str(ndt) + "\n  \"observation_model\": "+str(obs) +"\n  \"ndt_matching\": "+str(matching) + "\n  \"eval_file_name\": " + str(obs) + "_" + str(res)+ "_" + ndt_str +"_"+ ndt_match_str +"_"+str(dev)+"_"+"run_"+str(n)+ "\n")
                                    # stream.write(yaml.dump({'path_length': {'topics': [{'"/tf"', '"/scan_unified"'}]
                                    #                         'robot_bringup_launch': '"launch/all.launch"'
                                    #                         'wait_for_topics': '[]'
                                    #                         'wait_for_services': '[]'
                                    #                         'additional_parameters':
                                    #                           '"/use_sim_time"': true
                                    #                         additional_arguments:
                                    #                           "int_res": 0.35
                                    #                           "part_num": 75
                                    #                           "ndt_match": true}, default_flow_style=False))
                                self.robots = self.robots + "\n" + "    - " + filename

        meta = open(self.file_path+"robots", 'wa')
        
        meta.write(self.robots)






if __name__ == '__main__':
    try:
        RM = robot_maker()
        RM.make_robots()
    except rospy.ROSInterruptException:
        pass
