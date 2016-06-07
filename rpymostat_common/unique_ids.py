"""
The latest version of this package is available at:
<http://github.com/jantman/rpymostat-common>

##################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of rpymostat-common, also known as rpymostat-common.

    rpymostat-common is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    rpymostat-common is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with rpymostat-common.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/rpymostat-common> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

import logging
import re
import uuid

logger = logging.getLogger(__name__)


class SystemID(object):
    """
    Determine and retrieve a unique system ID for the hardware this is running
    on.
    """

    # List of method names in this class to call when determining an ID
    # in :py:method:`.id_string`.
    id_methods = [
        'raspberrypi_cpu',
        'uuid_getnode'
    ]

    # regex to match Hardware line from /proc/cpuinfo
    proc_cpuinfo_hw_re = re.compile('^Hardware\s+:\s+(\w+)$',
                                    flags=re.MULTILINE | re.IGNORECASE)

    # regex to match Revision line from /proc/cpuinfo
    proc_cpuinfo_rev_re = re.compile('^Revision\s+:\s+(\w+)$',
                                     flags=re.MULTILINE | re.IGNORECASE)

    # regex to match Serial line from /proc/cpuinfo
    proc_cpuinfo_serial_re = re.compile('^Serial\s+:\s+(\w+)$',
                                        flags=re.MULTILINE | re.IGNORECASE)

    # /proc/cpuinfo Hardware values for RPi
    rpi_hardware = ['BCM2708', 'BCM2709']

    # map /proc/cpuinfo Revision value to string model name
    # thanks to http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    # for this information
    rpi_revisions = {
        'Beta': 'B (Beta) ? 256MB (Q1 2012 Beta Board)',
        '0002': 'B 1.0 256MB (Q1 2012)',
        '0003': 'B ECN0001 1.0 256MB (Q3 2012)',
        '0004': 'B 2.0 256MB (Q3 2012 Sony)',
        '0005': 'B 2.0 256MB (Q4 2012 Qisda)',
        '0006': 'B 2.0 256MB (Q4 2012 Egoman)',
        '0007': 'A 2.0 256MB (Q1 2013 Egoman)',
        '0008': 'A 2.0 256MB (Q1 2013 Sony)',
        '0009': 'A 2.0 256MB (Q1 2013 Qisda)',
        '000d': 'B 2.0 512MB (Q4 2012 Egoman)',
        '000e': 'B 2.0 512MB (Q4 2012 Sony)',
        '000f': 'B 2.0 512MB (Q4 2012 Qisda)',
        '0010': 'B+ 1.0 512MB (Q3 2014 Sony)',
        '0011': 'Compute Module 1.0 512MB (Q2 2014 Sony)',
        '0012': 'A+ 1.1 256MB (Q4 2014 Sony)',
        '0013': 'B+ 1.2 512MB (Q1 2015)',
        '0014': 'Compute Module 1.0 512MB (Q2 2014 Embest)',
        '0015': 'A+ 1.1 256MB (Embest)',
        'a01041': '2 Model B 1.1 1GB (Q1 2015 Sony)',
        'a21041': '2 Model B 1.1 1GB (Q1 2015 Embest)',
        '900092': 'Zero 1.2 512MB (Q4 2015 Sony)',
        '900093': 'Zero 1.3 512MB (Q2 2016)',
        'a02082': '3 Model B 1.2 1024MB (Q1 2016 Sony)',
        'a22082': '3 Model B 1.2 1024MB (Q1 2016)',
    }

    @property
    def id_string(self):
        """
        Find/calculate and return the unique system ID string for the hardware
        this is running on.

        Internally, this calls all method whose names are listed in
        :py:attr:`.id_methods`, in order, and returns the value of the first
        one that returned something other than None.

        :return: unique, never-changing system ID
        :rtype: str
        """
        id_str = None
        for meth_name in self.id_methods:
            try:
                s = getattr(self, meth_name)()
                if s is not None:
                    id_str = s
                    logger.debug('Determined SystemID via method %s', meth_name)
                    break
            except Exception:
                logger.debug('Exception encountered when trying to determine '
                             'system ID via method %s', meth_name,
                             exc_info=1)
        # use the fallback
        if id_str is None:
            id_str = self.random_fallback()
            logger.debug('Determined SystemID via method random_fallback')
        logger.debug('Host ID: %s', id_str)
        return id_str

    def raspberrypi_cpu(self):
        """
        If this system is a Raspberry Pi, get its model and (CPU) serial number.

        Thanks to:
        http://elinux.org/RPi_HardwareHistory#Board_Revision_History

        :return: RaspberryPi serial number
        :rtype: str
        """
        with open('/proc/cpuinfo', 'r') as fh:
            lines = fh.read()
        hw_match = self.proc_cpuinfo_hw_re.search(lines)
        rev_match = self.proc_cpuinfo_rev_re.search(lines)
        serial_match = self.proc_cpuinfo_serial_re.search(lines)
        serial = 'unknown'
        if serial_match is not None:
            serial = serial_match.group(1).strip('0 ')

        # check Hardware from /proc/cpuinfo
        if hw_match is None:
            logger.debug('Not RPi - hw_match is None')
            return None
        if hw_match.group(1) not in self.rpi_hardware:
            logger.debug('Not RPi (Hardware: %s)', hw_match.group(1))
            return None
        logger.debug('Appears to be a Raspberry Pi (Hardware: %s)',
                     hw_match.group(1))

        # check Revision to get model
        if rev_match is None:
            return 'RaspberryPi/unknown_model/%s' % serial

        # find model
        if rev_match.group(1) not in self.rpi_revisions:
            return 'RaspberryPi/model_%s/%s' % (rev_match.group(1), serial)
        return 'RaspberryPi/%s/%s' % (self.rpi_revisions[rev_match.group(1)],
                                      serial)

    def uuid_getnode(self):
        """
        Determine this system's UUID via Python's :py:func:`uuid.getnode` (slow)
        method.

        :return: hardware system ID from Python's :py:func:`uuid.getnode`
        :rtype: str
        """
        return 'uuid.getnode_%x' % uuid.getnode()

    def random_fallback(self):
        """
        Generate a host ID using a random UUID via Python's
        :py:func:`uuid.uuid4`. Used as a fallback when the ID can't be
        determined using any other method.

        :return: random UUID
        :rtype: str
        """
        logger.warning('Could not determine system ID with any concrete method;'
                       ' using a random UUID.')
        return uuid.uuid4().hex
