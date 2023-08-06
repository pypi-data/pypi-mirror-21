This packages provides Zope 3 browser views for some generic exceptions.


.. contents::

System Errors
=============

System Errors are errors representing a system failure.  At the
application level, they are errors that are uncaught by the
application and that a developer hasn't provided a custom error view
for.

Zope provides a default system error view that prints an obnoxius
terse message and that sets the response status.

There is a simple view registered in ``ftesting.zcml`` which raises
``Exception()``:

  >>> print(http(r"""
  ... GET /error.html HTTP/1.1
  ... """))
  HTTP/1.0 500 Internal Server Error
  ...
    A system error occurred.
  ...

Another way of getting a system error is the occurrence of a system
error, such as ``ComponentLookupError``. I have registered a simple
view in ``ftesting.zcml``, too, that will raise a component lookup
error. So if we call ``componentlookuperror.html``, we should get the
error message:

  >>> print(http(r"""
  ... GET /componentlookuperror.html HTTP/1.1
  ... """))
  HTTP/1.0 500 Internal Server Error
  ...
    A system error occurred.
  ...


CHANGES
=======

4.0.0 (2017-05-01)
------------------

- Add support for PyPy, and Python 3.4, 3.5 and 3.6.

- Remove test dependency on ``zope.app.testing``,
  ``zope.app.zcmlfiles`` and many others.

3.6.3 (2011-05-23)
------------------

- Replaced an undeclared test dependency on ``zope.app.authentication`` with
  ``zope.password``.


3.6.2 (2010-09-14)
------------------

- No longer depend on ``zope.app.zptpage`` for tests.

- Replaced dependency on ``zope.app.securitypolicy`` by
  ``zope.securitypolicy``.


3.6.1 (2010-01-08)
------------------

- Require zope.browserpage which now contains ``namedtemplate``.

- Fix ftesting.zcml due to ``zope.securitypolicy`` update.

- Fix tests using a newer zope.publisher that requires zope.login.

3.6.0 (2009-05-18)
------------------

- ``ISystemErrorView`` interface has been moved to
  ``zope.browser.interfaces``, leaving BBB import here.

- Cut dependency on ``zope.formlib`` by requiring newer version of
  ``zope.app.pagetemplate`` which now contains ``namedtemplate``.


3.5.0 (2009-04-06)
------------------

- Use new ``zope.authentication`` instead of ``zope.app.security``.

- Removed deprecated code and thus removed dependency on zope.deferredimport.

- Removed old zpkg-related SETUP.cfg file.

3.4.2 (2009-01-27)
------------------

- Substitute zope.app.zapi by direct calls to its wrapped apis. See
  bug 219302.

- Fixed author email and home page.


3.4.1 (2007-10-31)
------------------

- Resolve ``ZopeSecurityPolicy`` deprecation warning.


3.4.0 (2007-10-24)
------------------

- Initial release independent of the main Zope tree.


