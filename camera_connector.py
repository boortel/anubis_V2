
from camera_vimba import Camera_vimba
import time

class Camera_connector:
    """!@brief This class is used to offer a bridge between a user interface and implemented
    mechanisms for connecting various cameras
    @details All connected cameras are stored within instance of this class and the class communicate
    with different mechanism by implementing them as a children of the camera_template class"""
    def __init__(self):
        ##Instances of camera control mechanisms. These are used only to list available cameras
        self.mech1 = Camera_vimba()
        #self.mech2 = Camera_harvester()
        
        ##Dictionary of mechanisms created above. Is used for easier manipulation with given objects
        self.mechanisms = { 
            self.mech1.get_name(): self.mech1,
            #self.mech2.get_name(): self.mech2
        }

        ##List of currently detected devices
        self.detected_devices = []

        ##Gentl producer paths used by Harvester mechanism
        self.producer_paths = []

        ##Holds all actively connected cameras
        self.active_devices = {}
        ##Number of devices connected while application was running. Will always only increment. Serves as a unique identifier for a device
        self.active_devices_count = 0

    def search_for_cameras(self):
        """!@brief Connected camera discovery
        @details Uses all implemented mechanisms to discover all connected cameras
        @return List of Dictionaries cantaining informations about cameras
        """
        self.detected_devices.clear()
        for mechanism in self.mechanisms:
            devices = self.mechanisms[mechanism].get_camera_list()
            name = self.mechanisms[mechanism].get_name()
            for device in devices:
                device["mechanism"] = name
                self.detected_devices.append(device)
            
            
        return self.detected_devices

    def select_camera(self, mechanism, device_id):
        """!@brief choose camera to connect to
        @details Select camera you will be using and set Camera object accordingly
        @param[in] mechanism Mechanism that should establish the connection
        @param[in] device_id ID of a camera you want to connect to
        """
        #self.mechanisms[mechanism].select_camera(device_id)
        if(mechanism == "Vimba"):
            self.active_devices[str(self.active_devices_count)] = Camera_vimba()

        
        self.active_devices[str(self.active_devices_count)].create_queues(str(self.active_devices_count))    
        self.active_devices[str(self.active_devices_count)].get_camera_list()
        self.active_devices[str(self.active_devices_count)].select_camera(device_id)
        self.active_devices_count += 1

        return str(self.active_devices_count - 1)

    def disconnect_camera(self, device):
        """!@brief Disconnect camera removes active camera object"""
        if device in self.active_devices.keys():
            self.active_devices[str(device)].disconnect_camera()
            self.active_devices.pop(str(device))
