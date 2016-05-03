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
        from bridge.hmd.openvr import HMD
        return HMD

    def init(self, context):
        """
        Initialize device

        :return: return True if the device was properly initialized
        :rtype: bool
        """
        try:
            HMD = self._getHMDClass()
            self._hmd = HMD()

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
            self.error("init", E, True)
            self._hmd = None
            return False

        else:
            return True
