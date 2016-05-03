"""
OpenVR Compatible (HTC Vive)
=============

OpenVR Compatible head mounted display
It uses a python wrapper to connect with the SDK
"""

from . import HMD_Base

from .oculus import Oculus

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
