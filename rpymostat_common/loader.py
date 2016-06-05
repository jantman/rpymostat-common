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
import re

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


def list_classes(classes):
    """
    Given a list of class objects, print their names, along with their
    _description attributes (if present) and any arguments they accept. Used in
    building dynamic CLI help.
    """
    for cls in classes:
        if hasattr(cls, '_description'):
            print('%s (%s)' % (cls.__name__, cls._description))
        else:
            print(cls.__name__)
        v = _get_varnames(cls)
        if len(v) == 0:
            print("")
            continue
        for vname in sorted(v.keys()):
            print("    %s - %s" % (vname, v[vname]))
        print("")


def _parse_docstring(docstring):
    """
    Given a docstring, attempt to parse out all ``:param foo:`` and
    ``:type foo:`` directives and their matching strings, collapsing
    whitespace. Return a dict of keys 'params' and 'types', each being a
    dict of name to string.

    :param docstring: docstring to parse
    :type docstring: str
    :rtype: dict
    """
    param_re = re.compile(
        r'^\s*:param ([^:]+):((?:(?!:param|:type|:return|:rtype).)*)',
        re.S | re.M
    )
    type_re = re.compile(
        r'^\s*:type ([^:]+):((?:(?!:param|:type|:return|:rtype).)*)',
        re.S | re.M
    )
    whitespace_re = re.compile(r'\s+')

    res = {'params': {}, 'types': {}}

    for itm in param_re.finditer(docstring):
        res['params'][itm.group(1).strip()] = whitespace_re.sub(
            ' ', itm.group(2).strip())
    for itm in type_re.finditer(docstring):
        res['types'][itm.group(1).strip()] = whitespace_re.sub(
            ' ', itm.group(2).strip())
    return res


def _get_varnames(klass):
    """
    Return a dict of variable names that klass's init method takes,
    to string descriptions of them (if present).

    :param klass: the class to get varnames for (from its __init__ method)
    :type klass: abc.ABCMeta
    :return: dict
    """
    func = klass.__init__.im_func
    res = {}
    args = []
    kwargs = {}
    if func.func_defaults is not None and len(func.func_defaults) > 0:
        if len(func.func_defaults) >= len(func.func_code.co_varnames)-1:
            args = []
            kwarg_names = func.func_code.co_varnames[1:]
        else:
            args = func.func_code.co_varnames[1:len(func.func_defaults)+1]
            kwarg_names = func.func_code.co_varnames[
                          len(func.func_defaults)+1:
            ]
        for x, _default in enumerate(func.func_defaults):
            kwargs[kwarg_names[x]] = func.func_defaults[x]
    else:
        args = func.func_code.co_varnames[1:]
    docstr = _parse_docstring(func.__doc__)
    for argname in args:
        s = ''
        if argname in docstr['types']:
            s = '(%s) ' % docstr['types'][argname]
        if argname in docstr['params']:
            s += docstr['params'][argname]
        res[argname] = s
    for argname, _default in kwargs.iteritems():
        s = ''
        if argname in docstr['types']:
            s = '(%s) ' % docstr['types'][argname]
        if argname in docstr['params']:
            s += docstr['params'][argname]
        res['%s=%s' % (argname, _default)] = s
    return res
