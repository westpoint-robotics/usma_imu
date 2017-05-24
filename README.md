# usma_xsens

This package extends https://github.com/ethz-asl/ethzasl_xsens_driver.git, do not install this package. The extension allows the usage of the xsens 4th generation protocol. In the USMA extension of the code both mtnode.py and mtnode_new.py are kept and many of the conventions from the original source are kept. For our purpose we are interested in running the mtnode_new.py node.

#### Initial Configuration
* The xsens must be properly configured to work with either this package or the original package. If not properly configured the packages generates parsing errors and stops execution.
* To initialize Xsens MTiG-710 for the first time, use the MT Manager Software on Windows or Ubuntu.
* Click on the icon with a lightning and wrench symbol ("Show the output configuration options for the selected device") and in the pop-up window, configure the following settings:
![alt text](https://github.com/westpoint-robotics/usma_xsens/blob/master/MT-Manager.png)
1. Normal Mode
2. TimeStamp: check "Packet Counter", check "Sample Time Fine"
3. Orientation: Quaternion,Floating Point 32-bit, 100hz
4. Inertial Data: check "Rate of Turn, Floating Point 32-bit, 100hz. check "deltaV", check "Acceleration"
5. Magnetic field: check "Magnetic Field", Floating Point 32-bit, 100hz
6. Temperature: check "Temperature", Floating Point 32-bit, 100hz
7. Pressure: check "Barometric Pressure", Floating Point 32-bit, 100hz
8. Sensor Component Readout: All blank.
9. Status: check "Status Word"
10. Position and Velocity: All blank.
11. GNSS Data: check "Pvt Data", check SatInfo, 4hz

#### Install umsa_xsens if using the xsens IMU/GPS.
1. `cd ~/catkin_ws/src`
2. `git clone https://github.com/westpoint-robotics/usma_xsens.git`
3. `sudo apt-get install ros-indigo-gps-common libpcap0.8-dev`
4. `sudo su`
5. `echo 'SUBSYSTEM=="tty", ATTRS{idProduct}=="0017", ATTRS{idVendor}=="2639", ATTRS{manufacturer}=="Xsens", SYMLINK+="mti700", ACTION=="add", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-xsens.rules`
6. `echo 'SUBSYSTEM=="tty", ATTRS{idProduct}=="0003", ATTRS{idVendor}=="2639", ATTRS{manufacturer}=="Xsens", SYMLINK+="mti300", ACTION=="add", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-xsens.rules`
7. `udevadm control --reload-rules`
8. `exit`
9. `cd ~/catkin_make`
10. `catkin_make`

####  To test the code.

* For the MTI700:

`roslaunch xsens_driver mti700.launch`

* For the MTI300:

`roslaunch xsens_driver mti300.launch`

##### This node publishes the following topics, accuracy still needs to be verified on some:
* /analog_in1	# Undetermined
* /analog_in2	# Undetermined
* /diagnostics  # Working
* /fix  	# Working
* /fix_extended # Working
* /imu/data  	# Working
* /imu_data_str # Working
* /magnetic  	# Working
* /pressure  	# NOT WORKING
* /temperature  # Working
* /velocity  	# Publishes angular velocities only


========================================================================================

* TODO: Not all the data coming from the device is published as a ROS Message. Need
to add more of it to the topics being published. This driver still needs more work
to enable it to handle the various different configurations.
* TODO: Look to standardize on TF2 instead of TF. See: http://wiki.ros.org/tf2/Migration

