Official Django client for Replyify
===================================

A Django wrapper for Replyify's Python API bindings.

Installation
------------

You can install this package by using the pip tool and installing:

::

    $ pip install django-replyify-oauth2

Or:

::

    $ easy_install django-replyify-oauth2

Register Your Application with Replyify
---------------------------------------

-  Sign up for Replyify at https://app.replyify.com/access/signup

-  Register your application at
   https://app.replyify.com/oauth2/applications/register

   -  Supported OAuth2 configuration is Public / Authorization code.

Configure the django-replyify-oauth2 module
-------------------------------------------

From your previously configured app, found at https://app.replyify.com/oauth2/applications add the following to your Django `settings.py`:
::
	REPLYIFY_CLIENT_ID = '{ update me }'
	REPLYIFY_CLIENT_SECRET = '{ update me }'
	REPLYIFY_USER_ID_FIELD = 'id'  # or other primary key user field like `guid`

	INSTALLED_APPS = [
		...
		'replyify_oauth2',
		...
	]

And add the following to your `urls.py`
::
	from django.conf.urls import patterns, include, url
	urlpatterns = patterns(
		...
		url(r'^replyify/', include('replyify_oauth2.urls', namespace='replyify')),
		...
	)

Run migrate
::

	$ python manage.py migrate

In templates
::
	<a href="{% url 'replyify:authorize' %}?next={% url 'home'|urlencode %}">Connect to Replyify</a>

Note: you can pass `next` query parameter to the authorize view to direct the user to correct page after OAuth flow has completed successfully.  Default will send user to '/'

In views as a decorator: this will kick off the Authorization flow or Refresh request (if token is expired) and will send the user back to the original requested url on completion
::
	from replyify_oauth2.decorators import replyify_auth_required

	@replyify_auth_required
	def my_view_that_needs_replyify(request):
		...

Using the Replyify API
----------------------

Documentation for the python bindings can be found here:

-  https://app.replyify.com/api/docs
-  http://replyify.com/api/docs/python

In the standard documentation (the first link), most of the reference
pages will have examples in Replyify's official bindings (including
Python). Just click on the Python tab to get the relevant documentation.

In the full API reference for python (the second link), the right half
of the page will provide example requests and responses for various API
calls.
