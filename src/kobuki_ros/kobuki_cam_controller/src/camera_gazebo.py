#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv

class OpenCVNode(Node):
    def __init__(self):
        super().__init__("OpenCVNode")
        
        self.subscriber_ = self.create_subscription(Image, "/depth_camera/color/image_raw", self.ImageCallback, 10)
        self.br = CvBridge()
        
        self.model = YOLO('/home/nilton/Desktop/Ros2_Projects/Kobuki/src/kobuki_ros/kobuki_cam_controller/src/best.pt')
        self.bounding_box_annotator = sv.BoxAnnotator()

    def ImageCallback(self, msg):
        try:
            frames = self.br.imgmsg_to_cv2(msg, "bgr8")
            # gray_frame = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

            results = self.model(frames)[0]
            detections = sv.Detections.from_ultralytics(results)

            image = self.bounding_box_annotator.annotate(scene=frames, detections=detections)

            # cv2.imshow('rgb', color_image)

            # Convert to ROS Image message
            cv2.imshow("Camera", image)
            cv2.waitKey(10)

        except Exception as e:
            self.get_logger().error(f'Error in ImageCallback: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = OpenCVNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
