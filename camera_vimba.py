from camera_template import Camera_template
from config_level import Config_level
from vimba import *
import global_queue
import copy
import global_vimba
import time
import threading
import vimba

class Camera_vimba(Camera_template):

    def __init__(self):
        super(Camera_vimba, self).__init__()

        self.name = "Vimba"
        self.cam = None

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

        self.flag_get_parameters.set() 
        self.flag_read_param_value.set()
        self.flag_set_parameter.set()
        self.flag_execute_command.set()
        self.flag_get_single_frame.set()
        self.flag_load_config.set()
        self.flag_save_config.set()
        self.flag_frame_producer.set()

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
                    
        #cams = self.vimba.get_all_cameras()
        #self.cam = cams[self.active_camera]
        #self.cam._open()
        #with global_vimba.v as vimba:
        #    self.cam = vimba.get_camera_by_id(self.selected_active_camera)
        
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
        
        with self.cam:
            while(not self.flag_disconnect.is_set() or not self.flag_frame_producer.is_set()):
                self.flag_loop.wait()
                self.flag_loop.clear()

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

    def _frame_handler(self,cam ,frame):
        """!@brief Defines how to process incoming frames
        @details Is defined for Vimba and defines how to acquire
            whole frame and put into the frame_queue
        """
        try:
            if not global_queue.frame_queue[self.cam_id].full() and frame.get_status() == FrameStatus.Complete:
                frame_copy = copy.deepcopy(frame)
                if self.is_recording:
                    global_queue.frame_queue[self.cam_id].put_nowait([frame_copy.as_opencv_image(),
                                            str(frame_copy.get_pixel_format())])
                global_queue.active_frame_queue[self.cam_id].put_nowait([frame_copy.as_opencv_image(),
                                               str(frame_copy.get_pixel_format())])
            else:
                pass
            cam.queue_frame(frame)
        except:
            pass

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
            self.params_read_param_value["return"] = getattr(self.cam, self.params_read_param_value["param_name"]).get()
            self.flag_read_param_value.set()
            return
        except:
            self.params_read_param_value["return"] = None
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
            getattr(self.cam, self.params_set_parameter["parameter_name"]).set(self.params_set_parameter["new_value"])
            self.params_set_parameter["return"] = True
        except (AttributeError, VimbaFeatureError):
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
        while(True):
            try:
                frame = self.cam.get_frame()
                pixel_format = str(frame.get_pixel_format())
                self.params_get_single_frame["return"] = [frame.as_opencv_image(), pixel_format]
                self.flag_get_single_frame.set()
                return
            except:
                pass
            
    
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
        return
        
    
    def __frame_producer(self):
        """!@brief Gets frames from camera while continuous acquisition is active
        @details Loads frames from camera as they come and stores them
            in a frame queue for consumer thread to process. The thread 
            runs until stream_stop_switch is set
        """
        
        self.flag_frame_producer.set()    
        self.cam.start_streaming(handler=self._frame_handler)
        
        self._stream_stop_switch.wait()
        
        while(True):
            try:
                self.cam.stop_streaming()
                return
            except VimbaCameraError as e:
                pass
        