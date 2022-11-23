from colorsys import rgb_to_hls
from src.camera_template import Camera_template
from src.config_level import Config_level
from vimba import *
import src.global_queue as global_queue
import copy
import src.global_vimba as global_vimba
import time
import threading
import vimba
import cv2
import numpy as np

class Camera_vimba(Camera_template):

    def __init__(self):
        super(Camera_vimba, self).__init__()

        self.name = "Vimba"
        self.cam = None
        self.pixel_conversion = None

        ##Flags to signalize request for some camera command, 
        # the request is then transfered to main object thread
        self.flag_get_parameters = threading.Event()
        self.flag_read_param_value = threading.Event()
        self.flag_set_parameter = threading.Event()
        self.flag_execute_command = threading.Event()
        self.flag_get_single_frame = threading.Event()
        self.flag_load_config = threading.Event()
        self.flag_save_config = threading.Event()
        self.flag_frame_producer = threading.Event()
        self.flag_loop = threading.Event()
        self.flag_disconnect = threading.Event()

        ##Setting all flags apart from loop and disconnect,
        # reason - they are activated by clearing instead of setting
        self.flag_get_parameters.set() 
        self.flag_read_param_value.set()
        self.flag_set_parameter.set()
        self.flag_execute_command.set()
        self.flag_get_single_frame.set()
        self.flag_load_config.set()
        self.flag_save_config.set()
        self.flag_frame_producer.set()

        ##Dictionaries holding information for its transfer between cam thread
        #and requesting thread
        self.params_get_parameters =   {'feature_queue':    "",
                                        'flag':             "",
                                        'visibility':       "",
                                        'return':           ""}
        self.params_read_param_value = {'param_name':       "",
                                        'return':           ""}
        self.params_set_parameter =    {'parameter_name':   "",
                                        'new_value':        "",
                                        'return':           ""}
        self.params_execute_command =  {'command_feature':  "",
                                        'return':           ""}
        self.params_load_config =      {'path':             "",
                                        'return':           ""}
        self.params_save_config =      {'path':             "",
                                        'return':           ""}
        self.params_get_single_frame = {'return':           ""}

        ##Variable that will hold producer thread when the aquisition becomes active
        self.thread_producer = None
    
    def get_camera_list(self,):
        """!@brief Connected camera discovery
        @details Uses vimba instance to discover all connected cameras
        @return List of Dictionaries cantaining informations about cameras
        """
        self.devices_info.clear()
        cams = global_vimba.v.get_all_cameras()

        for index, camera in enumerate(cams):
            d = {   'id_': camera.get_id(),
                    'model': camera.get_model()
                    }
            self.devices_info.append(d)
        return self.devices_info
     
    def select_camera(self,selected_device):
        """!@brief choose camera to connect to
        @details Select camera you will be using and set Camera object accordingly
        @param[in] selected_device ID of a camera you want to connect to
        """
        cams = global_vimba.v.get_all_cameras()
        for index, camera in enumerate(cams):
            if(selected_device == camera.get_id()):
                self.active_camera = index
                self.selected_active_camera = camera.get_id()
                self.cam = camera
        
        with self.cam:
            try:
            #Makes sure that the camera won't send packets larger 
            #than the destination pc can raceive.
                self.cam.GVSPAdjustPacketSize.run()
                while not self.cam.GVSPAdjustPacketSize.is_done():
                    pass
            except (AttributeError, VimbaFeatureError):
                    pass

        self.thread_loop = threading.Thread(target=self.loop)
        self.thread_loop.setDaemon(True)
        self.thread_loop.start()

    def get_parameters(self,feature_queue, flag, visibility = Config_level.Unknown):
        """!@brief Read parameters from camera
        @details Loads all available camera parameters
        @param[in] feature_queue each parameter's dictionary is put into 
            this queue
        @param[in] flag used to signal that the method finished (threading object)
        @param[in] visibility Defines level of parameters that should be put in
            the queue
        @return True if success else False
        """
        self.params_get_parameters = {'feature_queue':    feature_queue,
                                        'flag':             flag,
                                        'visibility':       visibility}

        self.flag_get_parameters.clear()
        self.flag_loop.set()
        self.flag_get_parameters.wait()
        return self.params_get_parameters["return"]
    
    def read_param_value(self,param_name):
        """!@brief Used to get value of one parameter based on its name
        @param[in] param_name Name of the parametr whose value we want to read
        @return A value of the selected parameter
        """

        self.params_read_param_value = {'param_name': param_name}
        self.flag_read_param_value.clear()
        self.flag_loop.set()
        self.flag_read_param_value.wait()
        return self.params_read_param_value["return"]       
    
    def set_parameter(self,parameter_name, new_value):
        """!@brief Method for setting camera's parameters
        @details Sets parameter to value defined by new_value
        @param[in] parameter_name A name of the parameter to be changed
        @param[in] new_value Variable compatible with value key in parameter
        @return True if success else returns False
        """
        self.params_set_parameter = {'parameter_name': parameter_name,
                                    'new_value':        new_value}
        self.flag_set_parameter.clear()
        self.flag_loop.set()
        self.flag_set_parameter.wait()
        return self.params_set_parameter["return"]
        
            
    def execute_command(self, command_feature):
        """@brief Execute command feature type
        @param[in] command_feature Name of the selected command feature
        """
        self.params_execute_command = {'command_feature': command_feature}
        self.flag_execute_command.clear()
        self.flag_loop.set()
        self.flag_execute_command.wait()
        return self.params_execute_command["return"]
        
    def get_single_frame(self,):
        """!@brief Grab single frame from camera
        @return Unmodified frame from camera
        """
        self.flag_get_single_frame.clear()
        self.flag_loop.set()
        self.flag_get_single_frame.wait()
        return self.params_get_single_frame["return"]
        
    def load_config(self,path):
        """!@brief Load existing camera configuration
        @param[in] path Defines a path and a name of the file containing the
            configuration of the camera
        @return True if success else False
        """
        self.params_load_config = {'path': path}
        self.flag_load_config.clear()
        self.flag_loop.set()
        self.flag_load_config.wait()
        return self.params_load_config["return"]

    def save_config(self,path):
        """!@brief Saves configuration of a camera to .xml file
        @param[in] path A path where the file will be saved
        """
        
        self.params_save_config = {'path': path}
        self.flag_save_config.clear()
        self.flag_loop.set()
        self.flag_save_config.wait()
        return self.params_save_config["return"]
    
    def _frame_producer(self):
        """!@brief Gets frames from camera while continuous acquisition is active
        @details Loads frames from camera as they come and stores them
            in a frame queue for consumer thread to process. The thread 
            runs until stream_stop_switch is set
        """
        self.flag_frame_producer.clear()
        self.flag_loop.set()
        self.flag_frame_producer.wait()       
                    
    def loop(self):  
        """!@brief Main loop for communication with camera object directly
        @details Only this loop has access to the camera, all user calls are transfered
        to this loop and handled here. This ensures that no race conditions will appear.
        """
        with self.cam:
            while(not self.flag_disconnect.is_set() or not self.flag_frame_producer.is_set()):
                #Wait until user asynchronously calls some camera method
                self.flag_loop.wait()
                self.flag_loop.clear()

                #chceck which method was called and handle it in this thread
                if(not self.flag_get_parameters.is_set()):
                    self._get_parameters()
                elif(not self.flag_read_param_value.is_set()):
                    self._read_param_value() 
                elif(not self.flag_set_parameter.is_set()):
                    self._set_parameter() 
                elif(not self.flag_execute_command.is_set()):
                    self._execute_command()    
                elif(not self.flag_get_single_frame.is_set()):
                    self._get_single_frame()  
                elif(not self.flag_load_config.is_set()):
                    self._load_config()  
                elif(not self.flag_save_config.is_set()):
                    self._save_config()  
                elif(not self.flag_frame_producer.is_set()):
                    self.thread_producer = threading.Thread(target=self.__frame_producer)
                    self.thread_producer.setDaemon(True)
                    self.thread_producer.start()            

    def _frame_handler(self, cam, frame):
        """!@brief Defines how to process incoming frames
        @details Is defined for Vimba and defines how to acquire
            whole frame and put into the frame_queue
        """
        format = cam.get_pixel_format()
        frame_copy = None
        frame_copy_save = None
        #try:
        if frame.get_status() == FrameStatus.Complete:
            if global_queue.frame_queue[self.cam_id].full():
                global_queue.frame_queue[self.cam_id].get_nowait()
                
            if not self.pixel_conversion[1] == None:  
                pixel_format = str(frame.get_pixel_format())
                
                frame_np = frame.as_numpy_ndarray()
                if "16" in pixel_format:
                    frame_np = frame_np/256
                elif "14" in pixel_format:
                    frame_np = frame_np/64
                elif "12" in pixel_format:
                    frame_np = frame_np/16
                elif "10" in pixel_format:
                    frame_np = frame_np/4

                if not self.pixel_conversion[0] == None:
                    frame_copy = copy.deepcopy(cv2.cvtColor(frame_np.astype(np.uint8), self.pixel_conversion[0]))
                    frame_copy_save = copy.deepcopy(cv2.cvtColor(frame.as_numpy_ndarray(), self.pixel_conversion[0]))
                else:
                    frame_copy = copy.deepcopy(frame_np.astype(np.uint8))
                    frame_copy_save = copy.deepcopy(frame.as_numpy_ndarray())
                
                format = self.pixel_conversion[1]

            else:
                frame_copy = copy.deepcopy(frame.as_opencv_image())
                frame_copy_save = copy.deepcopy(frame.as_opencv_image())
                format = str(frame.get_pixel_format())

            if self.is_recording:
                global_queue.frame_queue[self.cam_id].put_nowait([frame_copy_save,
                                        format])
            global_queue.active_frame_queue[self.cam_id].put_nowait([frame_copy,
                                            format])
            
        else:
            pass
        cam.queue_frame(frame)
        #except:
        #   print("EXCEPTION")

    def disconnect_camera(self):
        """!@brief Disconnect camera and restores the object to its initial state"""
        if(self.acquisition_running == True):
            self.stop_recording()
            self.thread_producer.join()

        self.flag_disconnect.set()
        self.flag_loop.set()
        self.thread_loop.join()
        global_queue.remove_frame_queue(self.cam_id)
        self.__init__()


    def _get_parameters(self):
        """!@brief Read parameters from camera
        @details Loads all available camera parameters
        @param[in] feature_queue each parameter's dictionary is put into 
            this queue
        @param[in] flag used to signal that the method finished (threading object)
        @param[in] visibility Defines level of parameters that should be put in
            the queue
        @return True if success else False
        """
        try:
            features = self.cam.get_all_features()
            for feature in features:
                feat_vis = int(feature.get_visibility())
                if(feat_vis > 0 and feat_vis <= self.params_get_parameters["visibility"] ):
                    name = feature.get_name()
                    
                    features_out = {}
                    features_out['name'] = name
                    
                    disp_name = feature.get_display_name()
                    features_out['attr_name'] = disp_name
                    
                    #if feature does not have read permission,
                    #go to next iteration
                    if(not feature.get_access_mode()[0]):
                        continue
                    
                    #Get feature's write mode
                    try:
                        attr = feature.get_access_mode()[1]
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_enabled'] = attr
                    
                    #Get feature's type if it exists
                    try:
                        attr = str(feature.get_type())
                        attr = attr.replace("<class 'vimba.feature.", '')
                        attr = attr.replace("'>","")
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_type'] = attr
                    
                    #Get availible enums for enum feature type
                    if(features_out['attr_type'] == "EnumFeature"):
                        try:
                            attr = feature.get_available_entries()
                        except (AttributeError, VimbaFeatureError):
                            attr = None
                    
                        features_out['attr_enums'] = attr
                    
                    #Get category for the feature
                    try:
                        attr = feature.get_category()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                
                    features_out['attr_cat'] = attr
                        
                    #Get feature's value if it exists
                    try:
                        attr = feature.get()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_value'] = attr
                    
                    #Get feature's range if it exists
                    try:
                        attr = feature.get_range()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_range'] = attr
                    
                    #Get feature's increment if it exists
                    try:
                        attr = feature.get_increment()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_increment'] = attr
                    
                    #Get feature's max length if it exists
                    try:
                        attr = feature.get_max_length()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_max_length'] = attr
                    
                    try:
                        attr = feature.get_tooltip()
                    except (AttributeError, VimbaFeatureError):
                        attr = None
                    
                    features_out['attr_tooltip'] = attr
                    
                    self.params_get_parameters["feature_queue"].put(features_out)
            self.params_get_parameters["flag"].set()

            self.params_get_parameters["return"] = True
            self.flag_get_parameters.set()
            return
        except:
            self.params_get_parameters["return"] = False
            self.flag_get_parameters.set()
            return
    
    def _read_param_value(self):
        """!@brief Used to get value of one parameter based on its name
        @param[in] param_name Name of the parametr whose value we want to read
        @return A value of the selected parameter
        """
        try:
            value = getattr(self.cam, self.params_read_param_value["param_name"]).get()
            type = str(getattr(self.cam, self.params_read_param_value["param_name"]).get_type())
            type = type.replace("<class 'vimba.feature.", '')
            type = type.replace("'>","")
            self.params_read_param_value["return"] = (value, type)
            self.flag_read_param_value.set()
            return
        except:
            self.params_read_param_value["return"] = (None, None)
            self.flag_read_param_value.set()
            return
    
    def _set_parameter(self):
        """!@brief Method for setting camera's parameters
        @details Sets parameter to value defined by new_value
        @param[in] parameter_name A name of the parameter to be changed
        @param[in] new_value Variable compatible with value key in parameter
        @return True if success else returns False
        """
        try:
            if self.params_set_parameter["parameter_name"] == "PixelFormat":
                self.cam.set_pixel_format(getattr(PixelFormat, self.params_set_parameter["new_value"]))
            else:
                print(self.params_set_parameter["new_value"])
                print(type(self.params_set_parameter["new_value"]))

                getattr(self.cam, self.params_set_parameter["parameter_name"]).set(self.params_set_parameter["new_value"])
            self.params_set_parameter["return"] = True
        except (AttributeError, VimbaFeatureError):
            print(f"error setting parameter {self.params_set_parameter['parameter_name']}")
            self.params_set_parameter["return"] = False

        self.flag_set_parameter.set()
        return
            
    def _execute_command(self):
        """@brief Execute command feature type
        @param[in] command_feature Name of the selected command feature
        """
        try:
            getattr(self.cam, self.params_execute_command["command_feature"]).run()
        except:
            pass

        self.flag_execute_command.set()
        return
    
    def _get_single_frame(self):
        """!@brief Grab single frame from camera
        @return Unmodified frame from camera
        """
        #while(True):     
        # 
        self._set_conversion_format()
        frame = self.cam.get_frame()
        pixel_format = None
        frame_copy = None

        if not self.pixel_conversion[1] == None:  
            pixel_format = str(frame.get_pixel_format())
            
            frame_np = frame.as_numpy_ndarray()
            if "16" in pixel_format:
                frame_np = frame_np/256
            elif "14" in pixel_format:
                frame_np = frame_np/64
            elif "12" in pixel_format:
                frame_np = frame_np/16
            elif "10" in pixel_format:
                frame_np = frame_np/4

            if not self.pixel_conversion[0] == None:
                frame_copy = copy.deepcopy(cv2.cvtColor(frame_np.astype(np.uint8), self.pixel_conversion[0]))
            else:
                frame_copy = copy.deepcopy(frame_np.astype(np.uint8))
            
            format = self.pixel_conversion[1]

        else:
            frame_copy = copy.deepcopy(frame.as_opencv_image())
            format = str(frame.get_pixel_format())
        
        self.params_get_single_frame["return"] = [frame_copy, format]
        self.flag_get_single_frame.set()
        return
            #try:
            #    frame = self.cam.get_frame()
            #    pixel_format = str(frame.get_pixel_format())
            #    self.params_get_single_frame["return"] = [frame.as_opencv_image(), pixel_format]
            #    self.flag_get_single_frame.set()
            #    return
            #except:
            #    pass
            
    def _load_config(self):
        """!@brief Load existing camera configuration
        @param[in] path Defines a path and a name of the file containing the
            configuration of the camera
        @return True if success else False
        """  
        try:
            self.cam.load_settings(self.params_load_config["path"], PersistType.NoLUT)
            self.flag_load_config.set()
            self.params_load_config["return"] = True
            return
        except:
            self.flag_load_config.set()
            self.params_load_config["return"] = False
            return
    
    def _save_config(self):
        """!@brief Saves configuration of a camera to .xml file
        @param[in] path A path where the file will be saved
        """
        self.cam.save_settings(self.params_save_config["path"], PersistType.NoLUT)

        self.flag_save_config.set()
        self.params_save_config["return"] = True
         
    def __frame_producer(self):
        """!@brief Gets frames from camera while continuous acquisition is active
        @details Loads frames from camera as they come and stores them
            in a frame queue for consumer thread to process. The thread 
            runs until stream_stop_switch is set
        """
        self.flag_frame_producer.set() 
        self._set_conversion_format()
        self.cam.start_streaming(handler=self._frame_handler)
                
        self._stream_stop_switch.wait()
        
        while(True):
            try:
                self.cam.stop_streaming()
                return
            except VimbaCameraError as e:
                pass

    def _set_conversion_format(self):
        format = str(self.cam.get_pixel_format())
        
        print(format)
#TODO Many conditions can be merged together 
        if(format == "Mono8"):
            self.pixel_conversion = [None, None]
        elif(format == "Mono10"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono10p"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono12"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono12p"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono14"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono16"):
            self.pixel_conversion = [None, "Mono8"]
        elif(format == "Mono12Packed"):
            self.pixel_conversion = [None, "Mono8"]
#RGB
        elif(format == "RGB8"):
            self.pixel_conversion = [cv2.COLOR_RGB2BGR, "BGR8"]
        elif(format == "RGB10"):
            self.pixel_conversion = [cv2.COLOR_RGB2BGR, "BGR8"]
        elif(format == "RGB12"):
            self.pixel_conversion = [cv2.COLOR_RGB2BGR, "BGR8"]
        elif(format == "RGB14"):
            self.pixel_conversion = [cv2.COLOR_RGB2BGR, "BGR8"]
        elif(format == "RGB16"):
            self.pixel_conversion = [cv2.COLOR_RGB2BGR, "BGR8"]
        elif(format == "BGR8"):
            self.pixel_conversion = [None, "BGR8"]
        elif(format == "BGR10"):
            self.pixel_conversion = [None, "BGR8"]
        elif(format == "BGR12"):
            self.pixel_conversion = [None, "BGR8"]
        elif(format == "BGR14"):
            self.pixel_conversion = [None, "BGR8"]
        elif(format == "BGR16"):
            self.pixel_conversion = [None, "BGR8"]
            
        elif(format == "BGRa8"):
            self.pixel_conversion = [cv2.COLOR_BGRA2RGBA, "RGBa8"]
        elif(format == "BGRa10"):
            self.pixel_conversion = [cv2.COLOR_BGRA2RGBA, "RGBa8"]
        elif(format == "BGRa12"):
            self.pixel_conversion = [cv2.COLOR_BGRA2RGBA, "RGBa8"]
        elif(format == "BGRa14"):
            self.pixel_conversion = [cv2.COLOR_BGRA2RGBA, "RGBa8"]
        elif(format == "BGRa16"):
            self.pixel_conversion = [cv2.COLOR_BGRA2RGBA, "RGBa8"]
         
        elif(format == "RGBa8"):
            self.pixel_conversion = [None, "RGBa8"]
        elif(format == "RGBa10"):
            self.pixel_conversion = [None, "RGBa8"]
        elif(format == "RGBa12"):
            self.pixel_conversion = [None, "RGBa8"]
        elif(format == "RGBa14"):
            self.pixel_conversion = [None, "RGBa8"]
        elif(format == "RGBa16"):
            self.pixel_conversion = [None, "RGBa8"]

        elif(format == "Argb8"):
            self.pixel_conversion = [None, "RGBa8"]   
#Bayer
        elif(format == "BayerRG8"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]
        elif(format == "BayerBG10"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGB10"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerGR10"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG10"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]

        elif(format == "BayerBG10p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGB10p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerGR10p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG10p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]

        elif(format == "BayerGB12"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerBG12"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGR12"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG12"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]
        
        elif(format == "BayerGB12p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerBG12p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGR12p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG12p"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]
        
        elif(format == "BayerBG16"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGB16"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerGR16"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG16"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]
        elif(format == "BayerBG8"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
        elif(format == "BayerGB8"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerGR8"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerGR12Packed"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GR2RGB, "BGR8"]
        elif(format == "BayerRG12Packed"):
            self.pixel_conversion = [cv2.COLOR_BAYER_RG2RGB, "BGR8"]
        elif(format == "BayerGB12Packed"):
            self.pixel_conversion = [cv2.COLOR_BAYER_GB2RGB, "BGR8"]
        elif(format == "BayerBG12Packed"):
            self.pixel_conversion = [cv2.COLOR_BAYER_BG2RGB, "BGR8"]
#YCBCR
        elif(format == "Yuv422"):
            self.pixel_conversion = [cv2.COLOR_YUV2RGB_Y422, "RGB8"]
        elif(format == "Yuv411"):
            self.pixel_conversion = [cv2.COLOR_YUV2RGB, "BGR8"]
        elif(format == "Yuv444"):
            self.pixel_conversion = [cv2.COLOR_YUV2BGR, "BGR8"]
        elif(format == "YCbCr411_8_CbYYCrYY"):
            self.pixel_conversion = [cv2.COLOR_YCrCb2RGB, "RGB8"]
        elif(format == "YCbCr422_8_CbYCrY"):
            self.pixel_conversion = [cv2.COLOR_YCrCb2RGB, "RGB8"]
        elif(format == "YCbCr8_CbYCr"):
            self.pixel_conversion = [cv2.COLOR_YCrCb2RGB, "RGB8"]
        else:
            self.pixel_conversion = [None, None]