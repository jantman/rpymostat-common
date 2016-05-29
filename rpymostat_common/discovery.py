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

logger = logging.getLogger(__name__)


def discover_engine():
    """
    Discover the RPyMostat Engine over the network, using mDNS / DNS-SD.

    :return: 2-tuple of (engine_addr, engine_port) if discovered before a
      timeout is reached, otherwise raise a DiscoveryTimeoutException.
    """
    raise NotImplementedError()


class EngineDiscoverer(object):
    """
    Class to discover RPyMostat Engine over the network (mDNS / Avahi / DNS-SD)
    """
    pass
