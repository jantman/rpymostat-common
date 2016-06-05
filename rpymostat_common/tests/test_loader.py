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

from rpymostat_common.loader import (
    load_classes, _get_varnames, _parse_docstring, list_classes
)

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT, mock_open, MagicMock  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT, mock_open, MagicMock  # noqa

pbm = 'rpymostat_common.loader'


class BaseClass(object):
    pass


class TestClass(BaseClass):

    _description = 'foo desc'

    def __init__(self, argOne, argTwo, kwarg1=None, kwarg2=1234):
        """
        Some text here
        About the init function

        Foo

        Bar.

        :param argOne: arg one info
        :type argOne: str
        :param argTwo: arg two info is a
          long
          line
        :type arg2: int
        :param kwarg1: kwarg1 info
        :type kwarg1: str
        :param kwarg2: kwarg2 info
        :return: foo
        """
        pass

    def sensors_present(self):
        return True

    def read(self):
        return {}


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

    def test_get_varnames(self):
        docstr = {
            'params': {
                'argOne': 'arg one info',
                'argTwo': 'arg two info is a long line',
                'kwarg1': 'kwarg1 info',
            },
            'types': {
                'argOne': 'str',
                'argTwo': 'int',
                'kwarg1': 'str'
            }
        }
        ds = """
        Some text here
        About the init function

        Foo

        Bar.

        :param argOne: arg one info
        :type argOne: str
        :param argTwo: arg two info is a
          long
          line
        :type arg2: int
        :param kwarg1: kwarg1 info
        :type kwarg1: str
        :param kwarg2: kwarg2 info
        :return: foo
        """
        with patch('%s._parse_docstring' % pbm) as mock_pd:
            mock_pd.return_value = docstr
            res = _get_varnames(TestClass)
        assert mock_pd.mock_calls == [call(ds)]
        assert res == {
            'argOne': '(str) arg one info',
            'argTwo': '(int) arg two info is a long line',
            'kwarg1=None': '(str) kwarg1 info',
            'kwarg2=1234': ''
        }

    def test_get_varnames_kwargs_only(self):

        class Foo(object):

            def __init__(self, foo=1, bar='two'):
                """mystr"""
                pass

        docstr = {
            'params': {
                'foo': 'arg one info',
                'bar': 'arg two info is a long line',
            },
            'types': {
                'foo': 'str',
            }
        }
        with patch('%s._parse_docstring' % pbm) as mock_pd:
            mock_pd.return_value = docstr
            res = _get_varnames(Foo)
        assert mock_pd.mock_calls == [call('mystr')]
        assert res == {
            'foo=1': '(str) arg one info',
            'bar=two': 'arg two info is a long line'
        }

    def test_get_varnames_no_default(self):

        class Foo(object):

            def __init__(self, arg1, arg2):
                """foo"""
                pass

        docstr = {
            'params': {
                'arg1': 'arg one info'
            },
            'types': {
                'arg1': 'str'
            }
        }
        with patch('%s._parse_docstring' % pbm) as mock_pd:
            mock_pd.return_value = docstr
            res = _get_varnames(Foo)
        assert mock_pd.mock_calls == [call("foo")]
        assert res == {
            'arg1': '(str) arg one info',
            'arg2': '',
        }

    def test_parse_docstring(self):
        docstring = """
        Some text here
        About the init function

        Foo

        Bar.

        :param argOne: arg one info
        :type argOne: str
        :param argTwo: arg two info is a
          long
          line
        :type argTwo: int
        :param kwarg1: kwarg1 info
        :type kwarg1: str
        :param kwarg2: kwarg2 info
        :return: foo
        """
        res = _parse_docstring(docstring)
        assert res == {
            'params': {
                'argOne': 'arg one info',
                'argTwo': 'arg two info is a long line',
                'kwarg1': 'kwarg1 info',
                'kwarg2': 'kwarg2 info'
            },
            'types': {
                'argOne': 'str',
                'argTwo': 'int',
                'kwarg1': 'str'
            }
        }

    def test_list_classes(self, capsys):
        varnames_one = {
            'argOne': '(int) arg one info',
            'argTwo': 'arg two info',
            'kwarg1=foo': '(str) kwarg1 info'
        }

        m1 = MagicMock(__name__='clsone', _description='desc1')
        m2 = MagicMock(__name__='cls2', _description='desc2')
        m3 = MagicMock(__name__='cls3')
        del(m3._description)

        def se_gv(klass):
            if klass == m1:
                return varnames_one
            return {}

        with patch('%s._get_varnames' % pbm) as mock_gv:
            mock_gv.side_effect = se_gv
            list_classes([m1, m2, m3])
        assert mock_gv.mock_calls == [call(m1), call(m2), call(m3)]
        expected_out = "clsone (desc1)\n"
        expected_out += "    argOne - (int) arg one info\n"
        expected_out += "    argTwo - arg two info\n"
        expected_out += "    kwarg1=foo - (str) kwarg1 info\n"
        expected_out += "\n"
        expected_out += "cls2 (desc2)\n\n"
        expected_out += "cls3\n\n"
        out, err = capsys.readouterr()
        assert err == ''
        assert out == expected_out
