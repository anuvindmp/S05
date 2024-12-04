import os
import rospy
import subprocess
import json
from std_srvs.srv import Trigger, TriggerResponse

# API details
API_URL = "https://detect.roboflow.com/ros-r2zc7/5?api_key=jdVJyYbHvAEkjyNaXGhv"

def call_yolo_service(req):
    """ROS service callback to interact with the YOLO API via curl."""
    # Path to the image file
    image_path = "~/catkin_ws/src/yolo_service/scripts/Cat_November_2010-1a.jpg"
    
    # Expand the tilde (~) to the full home directory path
    expanded_image_path = os.path.expanduser(image_path)

    try:
        # Prepare the base64 command to encode the image
        base64_command = ['base64', expanded_image_path]
        
        # Prepare the curl command to send the image to the YOLO API (suppress progress)
        curl_command = ['curl', '-s', '-d', '@-', 'https://detect.roboflow.com/ros-r2zc7/5?api_key=jdVJyYbHvAEkjyNaXGhv']

        # Open the subprocess for the base64 command and pipe the result to the curl command
        with subprocess.Popen(base64_command, stdout=subprocess.PIPE) as base64_process:
            with subprocess.Popen(curl_command, stdin=base64_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as curl_process:
                # Get the response and suppress curl transfer details
                response, error = curl_process.communicate()

                # Log any error from curl
                if error:
                    rospy.logerr(f"Error from curl: {error.decode('utf-8')}")
                    return TriggerResponse(success=False, message=error.decode('utf-8'))
                
                # Check if response is empty or invalid
                if not response:
                    rospy.logerr("No response received from the YOLO API.")
                    return TriggerResponse(success=False, message="No response received from the YOLO API.")

                # Assuming the response is in JSON format, parse it
                try:
                    response_json = json.loads(response.decode('utf-8'))

                    # Log the full response for debugging
                    rospy.loginfo(f"YOLO API response: {response_json}")

                    # Assuming the API returns a 'predictions' list with classification results
                    if 'predictions' in response_json:
                        # Extract the classification details
                        classifications = response_json['predictions']
                        result_message = f"Detected {len(classifications)} objects:\n"
                        for item in classifications:
                            result_message += f"Class: {item['class']} - Confidence: {item['confidence']}\n"
                        
                        rospy.loginfo(result_message)
                        return TriggerResponse(success=True, message=result_message)
                    else:
                        rospy.logwarn("No predictions in the response.")
                        return TriggerResponse(success=False, message="No predictions found in response.")
                except json.JSONDecodeError:
                    rospy.logerr("Failed to parse response JSON.")
                    return TriggerResponse(success=False, message="Failed to parse response JSON.")

    except Exception as e:
        rospy.logerr(f"Error calling YOLO API: {e}")
        return TriggerResponse(success=False, message=str(e))

def yolo_service_node():
    """Initialize the ROS service node."""
    rospy.init_node("yolo_service_node")
    rospy.Service("yolo_detect", Trigger, call_yolo_service)
    rospy.loginfo("YOLO detection service is ready.")
    rospy.spin()

if __name__ == "__main__":
    yolo_service_node()

