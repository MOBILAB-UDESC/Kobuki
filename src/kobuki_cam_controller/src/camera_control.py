#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class OpenCVNode(Node):
    def __init__(self):
        super().__init__("OpenCVNode")
        self.subscriber_ = self.create_subscription(Image, "/depth_camera/color/image_raw", self.ImageCallback, 10)
        self.br = CvBridge()
        self.face_cap = cv2.CascadeClassifier("/home/nilton/Desktop/kobuki_test/src/kobuki_cam_controller/src/haarcascade_frontalface_default.xml")

    def ImageCallback(self, msg):
        try:
            frame = self.br.imgmsg_to_cv2(msg, "bgr8")
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cap.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Camera", frame)
            cv2.waitKey(10)

        except Exception as e:
            self.get_logger().error(str(e))

def main(args=None):
    rclpy.init(args=args)
    node = OpenCVNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
