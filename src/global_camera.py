#    Anubis is a program to control industrial cameras and train and use artificial neural networks
#    Copyright (C) 2021 Lukaszczyk Jakub
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Global camera object
"""

from src.camera_connector import Camera_connector
import atexit

##Global camera object
cams = Camera_connector()
active_cam = ["-1", "-1", "-1", "-1"]

def close_cameras():
    """!@brief Function to properly disconnect all cameras when exiting the application
        """
    for index in range(cams.active_devices_count):
        cams.disconnect_camera(index)

atexit.register(close_cameras)

def change_active_cam(new, index):
    """!@brief Function is used to change the value of the global variable active_cam
        @param[in] new index of the active camera.
        """
    global active_cam
    active_cam[index] = new
