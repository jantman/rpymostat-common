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
import pkg_resources

logger = logging.getLogger(__name__)


def load_classes(entrypoint_name, superclass=None):
    """
    Attempt to load all pkg_resources entrypoints matching the given name,
    and return a list of the objects they load (usually classes). If
    ``superclass`` is specified, restrict the returned list to those which are
    subclasses of ``superclass``.

    :param entrypoint_name: name of the entrypoint to load
    :type entrypoint_name: str
    :param superclass: if specified, restrict the return value to only
      subclasses of this class / classinfo
    :type superclass: class or classinfo
    :return: list of loaded entrypoints (usually classes)
    :rtype: list
    """
    logger.debug("Loading classes for entrypoint: %s", entrypoint_name)
    classes = []
    for entry_point in pkg_resources.iter_entry_points(entrypoint_name):
        try:
            logger.debug("Trying to load class from entry point: %s",
                         entry_point.name)
            obj = entry_point.load()
            if superclass is None:
                classes.append(obj)
            elif issubclass(obj, superclass):
                classes.append(obj)
        except:
            logger.debug('Exception raised when loading entry point %s',
                         entry_point.name, exc_info=1)
    logger.debug("%s classes loaded successfully for entrypoint %s: %s",
                 len(classes), entrypoint_name, [c.__name__ for c in classes])
    return classes
