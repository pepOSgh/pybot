Platform for the development of Robotic applications based on Raspberry Pi(Rpi). Rpi is a credit card size computer, which given its size is easy to attach to robots of small size, like the one used in the tests. 

Project Structure

The "pybotConfig.xml"  is the platform configuration file.

The "robotConfig.xml" is the robot configuration file. In this file is described the robot's components and sensors. A series of supported actions by the robot are also specified.

In the bootstrap.py file states the platform booting secuence, loads the necesary modules and configurations from the xml configurations files. The platform supports two modes: PYBOT_TELECOMMAND and PYBOT_AUTONOMIC. In the first mode using the robot's supported actions defined inrobotConfig.xml, a properly logged user can control the robot using this actions. In the second mode, the robot executes the defined Behavior.

