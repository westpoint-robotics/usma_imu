# usma_xsens

This package extends https://github.com/ethz-asl/ethzasl_xsens_driver.git. The extension allows the usage of the xsens 4th generation protocol. The xsens must be properly configured to work either this package or the original package. If not properly configured the packages generate parsing errors and stop execution.

Use the MT Manager Software to configure the the Mti-G-700 to these settings:

* Normal Mode
* TimeStamp: check "Packet Counter", check "Sample Time Fine"
* Orientation: Quaternion,Floating Point 32-bit, 100hz
* Inertial Data: 	check "Rate of Turn, Floating Point 32-bit, 100hz
				check "deltaV", check "Acceleration"
* Magnetic field: check "Magnetic Field", Floating Point 32-bit, 100hz
* Temperature: check "Temperature", Floating Point 32-bit, 100hz
* Pressure: check "Barometric Pressure", Floating Point 32-bit, 100hz
* Sensor Component Readout: All blank.
* Status: check "Status Word"
* Position and Velocity: All blank.
* GNSS Data: check "Pvt Data", check SatInfo, 4hz

#### Install umsa_xsens if using the xsens IMU/GPS.
1. `cd ~/catkin_ws/src`
2. `git clone https://github.com/westpoint-robotics/usma_xsens.git`
3. `sudo apt-get install ros-indigo-gps-common libpcap0.8-dev`
4. `sudo su`
5. `echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="2639", ATTRS{manufacturer}=="Xsens", ATTRS{product}=="MTi-G-700 GPS/INS", SYMLINK+="xsens", ACTION=="add", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-xsens.rules`
6. `udevadm control --reload-rules`
7. `exit`
8. `cd ~/catkin_make`
9. `catkin_make`

========================================================================================

TODO: Not all the data coming from the device is published as a ROS Message. Need
to add more of it to the topics being published. This driver still needs more work
to enable it to handle the various different configurations.

