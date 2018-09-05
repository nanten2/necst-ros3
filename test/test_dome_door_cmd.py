#! /usr/bin/env python2

name = 'test_dome_door'

# ----
import time
import unittest
import rospy
import rostest
import std_msgs.msg


class TestDomeDoorCmd(unittest.TestCase):
    def setUp(self):
        self.recv_msg = None
        self.received = False
        
        rospy.init_node(name)
        self.timeout = rospy.get_param('~timeout')
        
        self.pub_cmd = rospy.Publisher(
            name = 'dome_door_cmd',
            data_class = std_msgs.msg.String,
            queue_size = 1,
        )
        
        self.pub_left = rospy.Publisher(
            name = 'dome_door_leftposition',
            data_class = std_msgs.msg.String,
            queue_size = 1,
            latch = True,
        )
        
        self.pub_right = rospy.Publisher(
            name = 'dome_door_rightposition',
            data_class = std_msgs.msg.String,
            queue_size = 1,
            latch = True,
        )
        
        self.pub_lock = rospy.Publisher(
            name = 'dome_door_lock',
            data_class = std_msgs.msg.Bool,
            queue_size = 1,
            latch = True,
        )
        
        self.sub = rospy.Subscriber(
            name = 'dome_door_cmd2',
            data_class = std_msgs.msg.String,
            callback = self.callback,
            queue_size = 1,
        )

        time.sleep(0.5)
        pass

    def callback(self, msg):
        self.recv_msg = msg
        self.received = True
        return

    def send(self, cmd, left, right, lock):
        self.received = False
        self.pub_cmd.publish(cmd)
        self.pub_left.publish(left)
        self.pub_right.publish(right)
        self.pub_lock.publish(lock)
        return
        
    def recv(self):
        start = time.time()
        while True:
            if self.received == True:
                break
            if time.time() - start > self.timeout:
                raise Exception('timeout')
            time.sleep(0.001)
            continue
        return self.recv_msg
    
    def test_open(self):
        # 1
        self.send('OPEN', 'OPEN', 'OPEN', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 2
        self.send('OPEN', 'CLOSE', 'OPEN', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 3
        self.send('OPEN', 'OPEN', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 4
        self.send('OPEN', 'CLOSE', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 5
        self.send('OPEN', 'MOVING', 'MOVING', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 6
        self.send('OPEN', 'OPEN', 'MOVING', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 7
        self.send('OPEN', 'CLOSE', 'MOVING', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 8
        self.send('OPEN', 'MOVING', 'OPEN', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 9
        self.send('OPEN', 'MOVING', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'OPEN')
        # 10
        self.send('OPEN', 'OPEN', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 11
        self.send('OPEN', 'CLOSE', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 12
        self.send('OPEN', 'OPEN', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 13
        self.send('OPEN', 'CLOSE', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 14
        self.send('OPEN', 'MOVING', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 15
        self.send('OPEN', 'OPEN', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 16
        self.send('OPEN', 'CLOSE', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 17
        self.send('OPEN', 'MOVING', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 18
        self.send('OPEN', 'MOVING', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        return

    def test_close(self):
        # 1
        self.send('CLOSE', 'OPEN', 'OPEN', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 2
        self.send('CLOSE', 'CLOSE', 'OPEN', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 3
        self.send('CLOSE', 'OPEN', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 4
        self.send('CLOSE', 'CLOSE', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 5
        self.send('CLOSE', 'MOVING', 'MOVING', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 6
        self.send('CLOSE', 'OPEN', 'MOVING', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 7
        self.send('CLOSE', 'CLOSE', 'MOVING', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 8
        self.send('CLOSE', 'MOVING', 'OPEN', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 9
        self.send('CLOSE', 'MOVING', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'CLOSE')
        # 10
        self.send('CLOSE', 'OPEN', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 11
        self.send('CLOSE', 'CLOSE', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 12
        self.send('CLOSE', 'OPEN', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 13
        self.send('CLOSE', 'CLOSE', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 14
        self.send('CLOSE', 'MOVING', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 15
        self.send('CLOSE', 'OPEN', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 16
        self.send('CLOSE', 'CLOSE', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 17
        self.send('CLOSE', 'MOVING', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 18
        self.send('CLOSE', 'MOVING', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        return

    def test_stay(self):
        # 1
        self.send('STAY', 'OPEN', 'OPEN', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 2
        self.send('STAY', 'CLOSE', 'OPEN', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 3
        self.send('STAY', 'OPEN', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 4
        self.send('STAY', 'CLOSE', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 5
        self.send('STAY', 'MOVING', 'MOVING', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 6
        self.send('STAY', 'OPEN', 'MOVING', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 7
        self.send('STAY', 'CLOSE', 'MOVING', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 8
        self.send('STAY', 'MOVING', 'OPEN', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 9
        self.send('STAY', 'MOVING', 'CLOSE', False)
        self.assertEqual(self.recv().data, 'STAY')
        # 10
        self.send('STAY', 'OPEN', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 11
        self.send('STAY', 'CLOSE', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 12
        self.send('STAY', 'OPEN', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 13
        self.send('STAY', 'CLOSE', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        # 14
        self.send('STAY', 'MOVING', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 15
        self.send('STAY', 'OPEN', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 16
        self.send('STAY', 'CLOSE', 'MOVING', True)
        self.assertRaises(Exception, self.recv)
        # 17
        self.send('STAY', 'MOVING', 'OPEN', True)
        self.assertRaises(Exception, self.recv)
        # 18
        self.send('STAY', 'MOVING', 'CLOSE', True)
        self.assertRaises(Exception, self.recv)
        return


if __name__=='__main__':
    rostest.rosrun('necst_ros3', 'test_dome_door_cmd', TestDomeDoorCmd)