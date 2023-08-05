# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

import os
import threading
import time
#from twisted.web.server import Site
#from twisted.web.resource import Resource
#from twisted.internet import reactor, endpoints


try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

import socket
from kervi.controller import Controller, UINumberControllerInput, UISwitchButtonControllerInput, UIButtonControllerInput, UISelectControllerInput
from kervi.utility.thread import KerviThread
import kervi.utility.nethelper as nethelper
import kervi.spine as spine
import kervi.hal as hal

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except:
    from http.server import SimpleHTTPRequestHandler

try:
    from BaseHTTPServer import HTTPServer
except:
    from http.server import HTTPServer


class _CameraPanInput(UINumberControllerInput):
    def __init__(self, controller):
        UINumberControllerInput.__init__(self, controller.component_id+".pan", "Pan", controller)
        self.unit = "degree"
        self.value = 0
        self.max_value = 90
        self.min_value = -90
        self.visible = False

    def value_changed(self, newValue, old_value):
        self.controller.pan_changed(newValue)

class _CameraTiltInput(UINumberControllerInput):
    def __init__(self, controller):
        UINumberControllerInput.__init__(self, controller.component_id+".tilt", "Tilt", controller)
        self.unit = "degree"
        self.value = 0
        self.max_value = 90
        self.min_value = -90
        self.visible = False

    def value_changed(self, newValue, old_value):
        self.controller.tilt_changed(newValue)

class _CameraFrameRate(UISelectControllerInput):
    """ Framerate selector """
    def __init__(self, controller):
        UISelectControllerInput.__init__(
            self,
            controller.component_id + ".framerate",
            "Framerate",
            controller
        )
        self.persist_value = True
        self.add_option("5", "5 / sec")
        self.add_option("10", "10 / sec")
        self.add_option("15", "15 / sec", True)

    def change(self, selected_options):
        if (len(selected_options)):
            value = selected_options[0]["value"]
            self.controller.framerate_changed(value)


class _CameraRecordButton(UISwitchButtonControllerInput):
    def __init__(self, controller):
        UISwitchButtonControllerInput.__init__(
            self, controller.component_id+".record",
            "Record",
            controller)
        self.set_ui_parameter("on_icon", "video-camera")
        self.set_ui_parameter("off_icon", "video-camera")
        self.set_ui_parameter("inline", True)
        self.set_ui_parameter("on_text", None)
        self.set_ui_parameter("off_text", None)
        self.set_ui_parameter("label", None)

    def on(self):
        self.controller.start_record()

    def off(self):
        self.controller.stop_record()

class _CameraPictureButton(UIButtonControllerInput):
    def __init__(self, controller):
        UIButtonControllerInput.__init__(
            self,
            controller.component_id+".savePicture",
            "Take picture",
            controller
        )
        self.set_ui_parameter("button_icon", "camera")
        self.set_ui_parameter("inline", True)

    def click(self):
        self.controller.save_picture()

class CameraBase(Controller):
    def __init__(self, camera_id, name, **kwargs):
        Controller.__init__(self, camera_id, name)
        self.type = "camera"
        self.add_input(
            _CameraPanInput(self),
            _CameraTiltInput(self),
            _CameraRecordButton(self),
            _CameraPictureButton(self),
            _CameraFrameRate(self)
        )

        self._ui_parameters["height"] = kwargs.get("height", 480)
        self._ui_parameters["width"] = kwargs.get("width", 640)
        self._ui_parameters["type"] = kwargs.get("type", "")
        self._ui_parameters["fps"] = kwargs.get("fps", 10)
        self._ui_parameters["source"] = kwargs.get("source", "")
        self._ui_parameters["show_pan_tilt"] = kwargs.get("show_pan_tilt", False)
        self._ui_parameters["show_buttons"] = kwargs.get("show_buttons", True)

    @property
    def height(self):
        """
        Height of images to capture
        """
        return self._ui_parameters["height"]

    @height.setter
    def height(self, value):
        self.set_ui_parameter("height", value)

    @property
    def width(self):
        """
        Width of images to capture
        """
        return self._ui_parameters["width"]

    @width.setter
    def width(self, value):
        self.set_ui_parameter("width", value)

    @property
    def fps(self):
        """
        Frames to capture per second
        """
        return self._ui_parameters["fps"]

    @fps.setter
    def fps(self, value):
        self.set_ui_parameter("fps", value)

    @property
    def source(self):
        """
        How to connect to this camera
        """
        return self._ui_parameters["source"]

    @source.setter
    def source(self, value):
        self.set_ui_parameter("source", value)


    def pan_changed(self, pan_value):
        """abstract method"""
        self.spine.log.debug(
            "abstract method pan_changed reached:{0}",
            self.component_id
        )

    def tilt_changed(self, tilt_value):
        """abstract method"""
        self.spine.log.debug(
            "abstract method tilt_frame reached:{0}",
            self.component_id
        )

    def framerate_changed(self, framerate):
        """abstract method"""
        self.spine.log.debug(
            "abstract method framerate_changed reached:{0}",
            self.component_id
        )

    def save_picture(self):
        """abstract method"""
        self.spine.log.debug(
            "abstract method save_picture reached:{0}",
            self.component_id
        )

    def start_record(self):
        """abstract method"""
        self.spine.log.debug(
            "abstract method start_record reached:{0}",
            self.component_id
        )

    def stop_record(self):
        """abstract method"""
        self.spine.log.debug(
            "abstract method stop_record reached:{0}",
            self.component_id
        )

    def link_to_dashboard(self, dashboard_id, section_id = None, **kwargs):
        r"""
        Links this camera to a dashboard section or to the background of a dashboard.

        :param dashboard_id:
            id of the dashboard to link to.
        :type section_id: str

        :param section_id:
            id of the section.
        :type section_id: str

        :param \**kwargs:
            Use the kwargs below to override default values set in ui_parameters

        :Keyword Arguments:
            * *ui_size* (``int``) -- Size of the component in dashboard unit size.
                In order to make the sections and components align correct a dashboard unit is defined.
                Default the dashboard unit is a square that is 150 x 150 pixels.
                The width of the camera picture is ui_size * dashboard unit size.

            * *show_buttons* (``bool``) -- Add this component to header of section.
            * *show_pan_tilt* (``bool``) -- Add this component to header of section.
        """
        if section_id is None:
            section_id = "background"
        
        Controller.link_to_dashboard(
            self,
            dashboard_id,
            section_id,
            **kwargs
            )

class _CameraFrameThread(KerviThread):
    def __init__(self, camera, mutex):
        KerviThread.__init__(self)
        self.spine = spine.Spine()
        self.alive = False
        self.camera = camera
        self.mutex = mutex
        if self.spine:
            self.spine.register_command_handler("startThreads", self._start_command)
            self.spine.register_command_handler("stopThreads", self._stop_command)
        #KerviThread.__init__(self)

    def run(self):
        """Private method do not call it directly or override it."""
        try:
            self.camera._capture_frames()
        except:
            self.spine.log.exception("CameraFrameThread")

    def _start_command(self):
        if not self.alive:
            self.alive = True
            KerviThread.start(self)

    def _stop_command(self):
        self.camera.terminate = True
        if self.alive:
            self.alive = False
            self.stop()


class _HTTPFrameHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        try:
            SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)
            self.server = server
            self.req = req
        except socket.error:
            pass

    def log_message(self, format, *args):
        return

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            #first_frame = True
            self.frame_number = 0
            while not self.server.camera._terminate:
                if self.server.camera.current_frame and self.server.camera.current_frame_number != self.frame_number:
                    self.frame_number = self.server.camera.current_frame_number
                    buf = BytesIO()
                    self.server.mutex.acquire()
                    try:
                        self.server.camera.current_frame.save(buf, format='jpeg')
                    finally:
                        self.server.mutex.release()

                    data = buf.getvalue()
                    self.wfile.write(b"--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(data))
                    self.end_headers()
                    self.wfile.write(data)
                    #first_frame = False
                time.sleep(1.0 / 30)
            return
        finally:
            pass


try:
    from socketserver import ThreadingMixIn
    class _HTTPFrameServer(ThreadingMixIn, HTTPServer):
        def __init__(self, addres, handler, camera, mutex):
            HTTPServer.__init__(self, addres, handler)
            self.camera = camera
            self.terminate = False
            self.mutex = mutex
except:
    print("ThreadingMixIn not found, use single thread camera server")
    class _HTTPFrameServer(HTTPServer):
        def __init__(self, addres, handler, camera, mutex):
            HTTPServer.__init__(self, addres, handler)
            self.camera = camera
            self.terminate = False
            self.mutex = mutex

class CameraStreamer(CameraBase):
    r"""
    Camera controller that streams video to the ui.

    :param camera_id:
        Id of the camera. The id is used to reference the camera in other parts of the kervi application.
    :type camera_id: str

    :param name:
        Name of the camera used in ui.
    :type name: str

    :param camera_source:
        A frame driver that is used to capture frames from a camera.

    :type camera_source: The name of the camera source to use.

    :param \**kwargs:
            See below

    :Keyword Arguments:
            * *height* (``int``) --
                Height of video frame. Default value is 480.

            * *width* (``int``) --
                Width of video frame. Default value is 640.

            * *fps* (``int``) --
                Frames per second.
    """
    def __init__(self, camera_id, name, camera_source = None, **kwargs):
        CameraBase.__init__(self, camera_id, name, type="frame", **kwargs)
        self._device_driver = hal.get_camera_driver(camera_source)
        self._device_driver.camera = self

        self.ip_address = nethelper.get_ip_address()
        self.ip_port = nethelper.get_free_port()
        self.source = "http://" + str(self.ip_address) + ":" + str(self.ip_port) + "/" + camera_id# + ".png"
        self.current_frame = None
        self.current_frame_number = 0

        from threading import Lock
        self.mutex = Lock()

        self.server = _HTTPFrameServer(
            (self.ip_address, self.ip_port),
            _HTTPFrameHandler,
            self,
            self.mutex
        )
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.frame_thread = _CameraFrameThread(self, self.mutex)

    @property
    def _terminate(self):
        """
        Flag to signal that the get_frames method should exit
        """
        return self._device_driver.terminate

    @_terminate.setter
    def _terminate(self, value):
        self._device_driver.terminate = value

    def get_font(self, name="Fanwood", size=16):
        """
        Returns a font that can be used by pil image functions.
        This default font is "Fanwood" that is available on all platforms.
        """
        import kervi
        from PIL import ImageFont
        kervipath = os.path.dirname(kervi.__file__)
        fontpath = os.path.join(kervipath, "fonts", name + ".otf")
        font = ImageFont.truetype(fontpath, size)
        return font

    def _capture_frames(self):
        self._device_driver.capture_frames()

    def _frame_ready(self, frame):
        if frame:
            self.mutex.acquire()
            self.current_frame = frame
            self.current_frame_number += 1
            self.mutex.release()

    def frame_captured(self, image):
        """
        Abstract method that is called when a new frame is ready from the camera.
        You can use this method to post process images before they are streamed.
        """
        pass


class IPCamera(CameraBase):
    def __init__(self, camera_id, name, dashboards, source):
        CameraBase.__init__(self, camera_id, name)
        self.parameters = {"height":480, "width":640, "source":source}

class USBCamera(CameraBase):
    def __init__(self, camera_id, name, dashboards, source):
        CameraBase.__init__(self, camera_id, name)
        self.parameters = {"height":480, "width":640, "source":source}


class FrameCameraDeviceDriver(object):
    """
    Base class for camera drivers that grap frames from a camera and streams them via the FrameCamera class.
    Could be used with the Raspberry PI camera.
    Fill in the abstract method capture_frames with functionality that graps
    frames from the camera and feeds them to the streamer.
    Frames must be pil images.
    """
    def __init__(self):
        self._terminate = False

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def terminate(self):
        return self._terminate

    @terminate.setter
    def terminate(self, value):
        self._terminate = value

    def capture_frames(self):
        """
        Abstract method use it like the run method in a thread.
        capture frames from camera until the flag self.terminate is True.
        captured frames should be passed to the method frame_ready.
        """
        raise NotImplementedError

    def wait_next_frame(self):
        """
        Waits for next frame.
        """
        time.sleep(1.0 / self.camera.fps)

    def frame_ready(self, frame):
        """
        Call this method when a frame is ready
        """
        self.camera._frame_ready(frame)
        