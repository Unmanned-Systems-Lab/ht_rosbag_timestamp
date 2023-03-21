#!/usr/bin/env python3

import rospy
import rosbag
import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
bag_name = 'QJ106-ChongQingYB-testground-1L1N20230316.bag' #被修改的bag名
out_bag_name = 'QJ106-ChongQingYB-testground-1L1N20230316-fix.bag' #修改后的bag名
dst_dir = '/media/ht/新加卷/rosbag/' #使用路径

with rosbag.Bag(dst_dir+out_bag_name, 'w') as outbag:
    stamp = None
    #topic:就是发布的topic msg:该topic在当前时间点下的message t:消息记录时间(非header)
    ##read_messages内可以指定的某个topic
    for topic, msg, t in rosbag.Bag(dst_dir+bag_name).read_messages():
        print(t)
        if topic == '/pointcloud_lidar3':
            stamp = msg.header.stamp
            # print('/pointcloud_lidar3')
        #针对没有header的文件，使用上面帧数最高的topic(即:/gps)的时间戳
        ##因为read_messages是逐时间读取，所以该方法可以使用
        elif topic == '/image_stamp' and stamp is not None: 
            outbag.write(topic, msg, stamp)
            continue
        #针对格式为Header的topic
        elif topic == '/image_time':
            outbag.write(topic, msg, msg.stamp)
            continue
        elif topic == "/localization_result":
            # print('/localization_result')
            outbag.write(topic, msg, stamp)
            continue
        #针对一般topic
        outbag.write(topic, msg, msg.header.stamp)

print("finished")
