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

import sys

from rpymostat_common.unique_ids import SystemID

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat_common.unique_ids'
pb = '%s.SystemID' % pbm


class TestSystemID(object):

    def setup(self):
        self.cls = SystemID()
        self.exc = RuntimeError()

    def se_exc(self, _self):
        raise self.exc

    def test_id_string(self):

        self.cls.id_methods = [
            'raspberrypi_cpu',
            'random_fallback',
            'uuid_getnode'
        ]
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch.multiple(
                pb,
                autospec=True,
                uuid_getnode=DEFAULT,
                random_fallback=DEFAULT,
                raspberrypi_cpu=DEFAULT,
            ) as mocks:
                mocks['raspberrypi_cpu'].return_value = None
                mocks['random_fallback'].side_effect = self.se_exc
                mocks['uuid_getnode'].return_value = 'uuidgetnode'
                res = self.cls.id_string
        assert res == 'uuidgetnode'
        assert mock_logger.mock_calls == [
            call.debug('Exception encountered when trying to determine system '
                       'ID via method %s', 'random_fallback', exc_info=1),
            call.debug('Determined SystemID via method %s', 'uuid_getnode'),
            call.debug('Host ID: %s', 'uuidgetnode')
        ]

    def test_id_string_fallback(self):

        self.cls.id_methods = [
            'raspberrypi_cpu',
            'random_fallback',
            'uuid_getnode'
        ]
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch.multiple(
                pb,
                autospec=True,
                uuid_getnode=DEFAULT,
                random_fallback=DEFAULT,
                raspberrypi_cpu=DEFAULT,
            ) as mocks:
                mocks['raspberrypi_cpu'].return_value = None
                mocks['random_fallback'].return_value = 'fallback'
                mocks['uuid_getnode'].return_value = None
                res = self.cls.id_string
        assert res == 'fallback'
        assert mock_logger.mock_calls == [
            call.debug('Determined SystemID via method %s', 'random_fallback'),
            call.debug('Host ID: %s', 'fallback')
        ]

    def test_uuid_getnode(self):
        with patch('%s.uuid.getnode' % pbm, autospec=True) as mock_getnode:
            mock_getnode.return_value = 163683361899416L
            res = self.cls.uuid_getnode()
        assert res == 'uuid.getnode_94de80a44398'
