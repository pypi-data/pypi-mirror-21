====================
Login/Logout Snippet
====================

The class LoginLogout:

  >>> from zope.app.security.browser.auth import LoginLogout

is used as a view to generate an HTML snippet suitable for logging in or
logging out based on whether or not the current principal is authenticated.

When the current principal is unauthenticated, it provides
IUnauthenticatedPrincipal:

  >>> from zope.authentication.interfaces import IUnauthenticatedPrincipal
  >>> from zope.principalregistry.principalregistry import UnauthenticatedPrincipal
  >>> anonymous = UnauthenticatedPrincipal('anon', '', '')
  >>> IUnauthenticatedPrincipal.providedBy(anonymous)
  True

When LoginLogout is used for a request that has an unauthenticated principal,
it provides the user with a link to 'Login':

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> request.setPrincipal(anonymous)
  >>> print(LoginLogout(None, request)())
  <a href="@@login.html?nextURL=http%3A//127.0.0.1">[Login]</a>

Attempting to login at this point will fail because nothing has
authorized the principal yet:

  >>> from zope.app.security.browser.auth import HTTPAuthenticationLogin
  >>> login = HTTPAuthenticationLogin()
  >>> login.request = request
  >>> login.context = None
  >>> login.failed = lambda: 'Login Failed'
  >>> login.login()
  'Login Failed'

There is a failsafe that will attempt to ask for HTTP Basic authentication:

  >>> from zope.app.security.browser.auth import HTTPBasicAuthenticationLogin
  >>> basic_login = HTTPBasicAuthenticationLogin()
  >>> basic_login.request = request
  >>> basic_login.failed = lambda: 'Basic Login Failed'
  >>> basic_login.login()
  'Basic Login Failed'
  >>> request._response.getHeader('WWW-Authenticate', literal=True)
  'basic realm="Zope"'
  >>> request._response.getStatus()
  401

Of course, an unauthorized principal is confirmed to be logged out:

  >>> from zope.app.security.browser.auth import HTTPAuthenticationLogout
  >>> logout = HTTPAuthenticationLogout(None, request)
  >>> logout.logout(nextURL="bye.html")
  'bye.html'
  >>> logout.confirmation = lambda: 'Good Bye'
  >>> logout.logout()
  'Good Bye'

Logout, however, behaves differently. Not all authentication protocols (i.e.
credentials extractors/challengers) support 'logout'. Furthermore, we don't
know how an admin may have configured Zope's authentication. Our solution is
to rely on the admin to tell us explicitly that the site supports logout.

By default, the LoginLogout snippet will not provide a logout link for an
unauthenticated principal. To illustrate, we'll first setup a request with an
unauthenticated principal:

  >>> from zope.security.interfaces import IPrincipal
  >>> from zope.interface import implementer
  >>> @implementer(IPrincipal)
  ... class Bob:
  ...     id = 'bob'
  ...     title = description = ''
  >>> bob = Bob()
  >>> IUnauthenticatedPrincipal.providedBy(bob)
  False
  >>> request.setPrincipal(bob)

In this case, the default behavior is to return None for the snippet:

  >>> print(LoginLogout(None, request)())
  None

And at this time, login will correctly direct us to the next URL, or
to the confirmation page:

  >>> login = HTTPAuthenticationLogin()
  >>> login.request = request
  >>> login.context = None
  >>> login.login(nextURL='good.html')
  >>> login.confirmation = lambda: "You Passed"
  >>> login.login()
  'You Passed'

Likewise for HTTP Basic authentication:

  >>> login = HTTPBasicAuthenticationLogin()
  >>> login.request = request
  >>> login.context = None
  >>> login.confirmation = lambda: "You Passed"
  >>> login.login()
  'You Passed'


To show a logout prompt, an admin must register a marker adapter that provides
the interface:

  >>> from zope.authentication.interfaces import ILogoutSupported

This flags to LoginLogout that the site supports logout. There is a 'no-op'
adapter that can be registered for this:

  >>> from zope.authentication.logout import LogoutSupported
  >>> from zope.component import provideAdapter
  >>> provideAdapter(LogoutSupported, (None,), ILogoutSupported)

Now when we use LoginLogout with an unauthenticated principal, we get a logout
prompt:

  >>> print(LoginLogout(None, request)())
  <a href="@@logout.html?nextURL=http%3A//127.0.0.1">[Logout]</a>

And we can log this principal out, passing a URL to redirect to:

  >>> logout = HTTPAuthenticationLogout(None, request)
  >>> logout.redirect = lambda: 'You have been redirected.'
  >>> logout.logout(nextURL="loggedout.html")
  'You have been redirected.'
