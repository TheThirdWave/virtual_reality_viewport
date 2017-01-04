"""
OpenVR Compatible (HTC Vive)
=============

OpenVR Compatible head mounted display
It uses a python wrapper to connect with the SDK
"""

from . import HMD_Base

from ..lib import (
        checkModule,
        )

class OpenVR(HMD_Base):
    def __init__(self, context, error_callback):
        super(OpenVR, self).__init__('OpenVR', True, context, error_callback)
        checkModule('hmd_sdk_bridge')

    def _getHMDClass(self):
        """
        This is the python interface to the DLL file in hmd_sdk_bridge.
        """
        from bridge.hmd.openvr import HMD
        return HMD

    @property
    def projection_matrix(self):
        if self._current_eye:
            matrix = self._hmd.getProjectionMatrixRight(self._near, self._far)
        else:
            matrix = self._hmd.getProjectionMatrixLeft(self._near, self._far)

        self.projection_matrix = matrix
        return super(OpenVR, self).projection_matrix

    @projection_matrix.setter
    def projection_matrix(self, value):
        self._projection_matrix[self._current_eye] = \
                self._convertMatrixTo4x4(value)


    def init(self, context):
        """
        Initialize device

        :return: return True if the device was properly initialized
        :rtype: bool
        """
        try:
            HMD = self._getHMDClass()
            self._hmd = HMD()

            # bail out early if we didn't initialize properly
            if self._hmd.get_state_bool() == False:
                raise Exception(self._hmd.get_status())

            # Tell the user our status at this point.
            self.status = "HMD Init OK. Make sure lighthouses running else no display."

            # gather arguments from HMD
            self.setEye(0)
            self.width = self._hmd.width_left
            self.height = self._hmd.height_left

            self.setEye(1)
            self.width = self._hmd.width_right
            self.height = self._hmd.height_right

            # initialize FBO
            if not super(OpenVR, self).init():
                raise Exception("Failed to initialize HMD")

            # send it back to HMD
            if not self._setup():
                raise Exception("Failed to setup OpenVR Compatible HMD")

        except Exception as E:
            self.error("OpenVR.init", E, True)
            self._hmd = None
            return False

        else:
            return True

    def _setup(self):
        return self._hmd.setup(self._color_texture[0], self._color_texture[1])

    def loop(self, context):
        """
        Get fresh tracking data
        """
        try:
            data = self._hmd.update()

            self._eye_orientation_raw[0] = data[0]
            self._eye_orientation_raw[1] = data[2]
            self._eye_position_raw[0] = data[1]
            self._eye_position_raw[1] = data[3]
            self._devices = data[4]
            self._constate1 = data[5]
            self._constate2 = data[6]
            self._conpos1 = data[7]
            self._conpos2 = data[8]
            # update matrices
            super(OpenVR, self).loop(context)

        except Exception as E:
            self.error("OpenVR.loop", E, False)
            return False

        #if VERBOSE:
        #    print("Left Eye Orientation Raw: " + str(self._eye_orientation_raw[0]))
        #    print("Right Eye Orientation Raw: " + str(self._eye_orientation_raw[1]))

        return True

    def frameReady(self):
        """
        The frame is ready to be sent to the device
        """
        try:
            self._hmd.frameReady()

        except Exception as E:
            self.error("OpenVR.frameReady", E, False)
            return False

        return True

    def reCenter(self):
        """
        Re-center the HMD device

        :return: return True if success
        :rtype: bool
        """
        return self._hmd.reCenter()

    def quit(self):
        """
        Garbage collection
        """
        self._hmd = None
        return super(OpenVR, self).quit()
