import sys, time, os, qi, math

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
        tts_service = session.service("ALTextToSpeech")
        motion_service  = session.service("ALMotion")
        posture_service = session.service("ALRobotPosture")
        audio_service = session.service("ALAudioDevice")
        leds_service = session.service("ALLeds")
    except Exception as e:
        print(f"Failed to load services: {e}")
        sys.exit(1)

    

    audio_service.setOutputVolume(50)
    # blue LEDs
    leds_service.fadeRGB("FaceLeds", 0x0000FF, 0.5)

    headJoints = ["HeadYaw", "HeadPitch"]
    headReset = [math.radians(0), math.radians(0)]
    headAngles = [math.radians(30), math.radians(-10)]

    motion_service.setAngles(headJoints, headAngles, 0.2)
    motion_service.setAngles(headJoints, headReset, 0.2)
    
    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Pose Init
    posture_service.goToPosture("Crouch", 0.5)
    posture_service.goToPosture("StandInit", 0.5)
    
    # green LEDs
    leds_service.fadeRGB("FaceLeds", 0x00FF00, 0.5)

    # introductory speech
    tts_service.say("Hello! My name is Nao! To perform the Three Good Things exercise, we can discuss three good things from your day. Let's try it out!")
    
    # Raise right arm
    motion_service.setAngles(
        ["RShoulderPitch", "RShoulderRoll", "RElbowRoll"],
        [math.radians(-30), math.radians(-10), math.radians(60)],
        0.2
    )

    time.sleep(1)

    # Wave forward/back 5 times
    for i in range(3):
        # Arm forward
        motion_service.setAngles(
            ["RShoulderPitch"],
            [math.radians(-60)],
            0.15
        )
        time.sleep(0.5)

        # Arm back
        motion_service.setAngles(
            ["RShoulderPitch"],
            [math.radians(-30)],
            0.15
        )
        time.sleep(0.5)

    
    # sit down
    posture_service.goToPosture("Sit", 0.5)
    
    # Rest Movement
    motion_service.rest()


if __name__ == "__main__":
    main()
