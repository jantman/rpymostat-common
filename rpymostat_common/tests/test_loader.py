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
import pkg_resources

from rpymostat_common.loader import load_classes

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT, mock_open  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT, mock_open  # noqa

pbm = 'rpymostat_common.loader'


class TestLoader(object):

    def test_load_classes(self):

        def se_exc(*args, **kwargs):
            raise Exception()

        class EP1(object):
            name = 'EP1'

        mock_ep1 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep1).name = 'ep1'
        mock_ep1.load.return_value = EP1

        class EP2(object):
            name = 'EP2'

        mock_ep2 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep2).name = 'ep1'
        mock_ep2.load.return_value = EP2

        class EP3(object):
            name = 'EP3'

        mock_ep3 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep3).name = 'ep3'
        mock_ep3.load.return_value = EP3

        mock_ep4 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep4).name = 'ep4'
        mock_ep4.load.side_effect = se_exc

        entry_points = [mock_ep1, mock_ep2, mock_ep3, mock_ep4]

        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch('%s.pkg_resources.iter_entry_points' % pbm,
                       autospec=True) as mock_iep:
                mock_iep.return_value = entry_points
                res = load_classes('my.entrypoint')
        assert res == [EP1, EP2, EP3]
        assert mock_iep.mock_calls == [call('my.entrypoint')]
        assert mock_logger.mock_calls == [
            call.debug('Loading classes for entrypoint: %s', 'my.entrypoint'),
            call.debug('Trying to load class from entry point: %s',
                       'ep1'),
            call.debug('Trying to load class from entry point: %s',
                       'ep1'),
            call.debug('Trying to load class from entry point: %s',
                       'ep3'),
            call.debug('Trying to load class from entry point: %s',
                       'ep4'),
            call.debug('Exception raised when loading entry point %s',
                       'ep4', exc_info=1),
            call.debug("%s classes loaded successfully for entrypoint %s: %s",
                       3, 'my.entrypoint', ['EP1', 'EP2', 'EP3'])
        ]

    def test_load_classes_with_superclass(self):

        class MySuperClass(object):
            pass

        class EP1(MySuperClass):
            name = 'EP1'

        mock_ep1 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep1).name = 'ep1'
        mock_ep1.load.return_value = EP1

        class EP2(object):
            name = 'EP2'

        mock_ep2 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep2).name = 'ep1'
        mock_ep2.load.return_value = EP2

        class EP3(MySuperClass):
            name = 'EP3'

        mock_ep3 = Mock(spec_set=pkg_resources.EntryPoint)
        type(mock_ep3).name = 'ep3'
        mock_ep3.load.return_value = EP3

        entry_points = [mock_ep1, mock_ep2, mock_ep3]

        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch('%s.pkg_resources.iter_entry_points' % pbm,
                       autospec=True) as mock_iep:
                mock_iep.return_value = entry_points
                res = load_classes('my.entrypoint', superclass=MySuperClass)
        assert res == [EP1, EP3]
        assert mock_iep.mock_calls == [call('my.entrypoint')]
        assert mock_logger.mock_calls == [
            call.debug('Loading classes for entrypoint: %s', 'my.entrypoint'),
            call.debug('Trying to load class from entry point: %s',
                       'ep1'),
            call.debug('Trying to load class from entry point: %s',
                       'ep1'),
            call.debug('Trying to load class from entry point: %s',
                       'ep3'),
            call.debug("%s classes loaded successfully for entrypoint %s: %s",
                       2, 'my.entrypoint', ['EP1', 'EP3'])
        ]
