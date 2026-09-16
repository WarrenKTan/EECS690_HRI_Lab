import sys, time, os, qi, math
import time

if len(sys.argv) > 1 and len(sys.argv) < 3:
    ROBOT_IP = sys.argv[1]
    ROBOT_PORT = 9559
else:
    print("please provide proper number of arguments")
    print("Proper program usage: python3 nao_introduction.py IP_ADDRESS_HERE")
    sys.exit(1)

def main():
    session = qi.Session()
    try:
        print(f"Connecting to NAO at {ROBOT_IP}:{ROBOT_PORT}...")
        session.connect(f"tcp://{ROBOT_IP}:{ROBOT_PORT}")
        print("Successfully connected to NAO!")
    except RuntimeError as e:
        print(f"Failed to connect to the robot at {ROBOT_IP}: {e}")
        print("Please try again")
        sys.exit(1)

    try:
        motion_service  = session.service("ALMotion")
        posture_service = session.service("ALRobotPosture")
    except Exception as e:
        print(f"Failed to load services: {e}")
        sys.exit(1)

    try:
        animate = session.service("ALBehaviorManager")
    except Exception as e:
        print(f"Failed to load ALBehaviorManager: {e}")
        animate = None


    startLen = len("animations/Stand/Gestures/")

    # stand up
    posture_service.goToPosture("Stand", 1.0)

    expressions = [
        # "animations/Stand/Gestures/Yes_1",
        # "animations/Stand/Gestures/Hey_1",
        # "animations/Stand/BodyTalk/Listening/Listening_2",
        # "animations/Stand/Gestures/Enthusiastic_1",
        # "animations/Stand/Gestures/Great_1",
        "animations/Stand/Gestures/Thinking_3",
        "animations/Stand/Gestures/Thinking_4",
        "animations/Stand/Gestures/Thinking_5",
        # "animations/Stand/Gestures/Applause_1"
    ]
    # cycle through expressions
    for expression in expressions:
        print(f"playing expression: {expression[startLen:]}")
        animate.startBehavior(expression)
        time.sleep(4)
    
    # sit down
    posture_service.goToPosture("Sit", 0.5)
    
    # Rest Movement
    motion_service.rest()


if __name__ == "__main__":
    main()
