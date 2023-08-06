# Copyright 2015 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Utility class for VM related operations on Hyper-V.
"""

from os_win._i18n import _


class OSWinException(Exception):
    msg_fmt = 'An exception has been encountered.'

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            message = self.msg_fmt % kwargs

        self.message = message
        super(OSWinException, self).__init__(message)


class NotFound(OSWinException):
    msg_fmt = _("Resource could not be found: %(resource)s")


class HyperVException(OSWinException):
    pass


# TODO(alexpilotti): Add a storage exception base class
class VHDResizeException(HyperVException):
    msg_fmt = _("Exception encountered while resizing the VHD %(vhd_path)s."
                "Reason: %(reason)s")


class HyperVAuthorizationException(HyperVException):
    msg_fmt = _("The Windows account running nova-compute on this Hyper-V "
                "host doesn't have the required permissions to perform "
                "Hyper-V related operations.")


class HyperVVMNotFoundException(NotFound, HyperVException):
    msg_fmt = _("VM not found: %(vm_name)s")


class HyperVPortNotFoundException(NotFound, HyperVException):
    msg_fmt = _("Switch port not found: %(port_name)s")


class SMBException(OSWinException):
    pass


class Win32Exception(OSWinException):
    msg_fmt = _("Executing Win32 API function %(func_name)s failed. "
                "Error code: %(error_code)s. "
                "Error message: %(error_message)s")

    def __init__(self, message=None, **kwargs):
        self.error_code = kwargs.get('error_code')
        super(Win32Exception, self).__init__(message=message, **kwargs)


class VHDException(OSWinException):
    pass


class VHDWin32APIException(VHDException, Win32Exception):
    pass


class FCException(OSWinException):
    pass


class FCWin32Exception(FCException, Win32Exception):
    pass


class WMIException(OSWinException):
    def __init__(self, message=None, wmi_exc=None):
        if wmi_exc:
            try:
                wmi_exc_message = wmi_exc.com_error.excepinfo[2].strip()
                message = "%s WMI exception message: %s" % (message,
                                                            wmi_exc_message)
            except AttributeError:
                pass
            except IndexError:
                pass
        super(WMIException, self).__init__(message)


class WqlException(OSWinException):
    pass


class ISCSITargetException(OSWinException):
    pass


class ISCSITargetWMIException(ISCSITargetException, WMIException):
    pass


class ISCSIInitiatorAPIException(Win32Exception):
    pass


class ISCSILunNotAvailable(ISCSITargetException):
    msg_fmt = _("Could not find lun %(target_lun)s "
                "for iSCSI target %(target_iqn)s.")


class Win32IOException(Win32Exception):
    pass


class DiskNotFound(NotFound):
    pass


class HyperVRemoteFXException(HyperVException):
    pass


class HyperVClusterException(HyperVException):
    pass


class JobTerminateFailed(HyperVException):
    msg_fmt = _("Could not terminate the requested job(s).")
