Django tool for create ont time links


Installation
============

For integrate with Django need to add *ua2.otl* to the list of installed app:


.. code-block:: python


	INSTALLED_APPS += (
		'ua2.otl')


and put into a root urls.py next line:

.. code-block:: python

    url(r'^l/', include('ua2.otl.urls'))


Be warning: include urls.py only compatibil with Django >= 1.8.
For django before 1.8 need use following solution:


.. code-block:: python

	from ua2.otl.views import otl_view

	urlpatterns = urlpatterns(
		.....
	    url(r'^l/(?P<otp_key>\w+)/$', otl_view, name='one-time-link'),
	)


Using
============


You can use *OneTimeLink* with several scenario:

* redirect to view with django backresolve (with support callback)
* redirect to direct URL (with support callback)
* using view to redner response


Redirects
---------

There are two way to pass resulted link to OneTimeLink object:

* pass url resolve point with kwargs
* pass rendered link


.. code-block:: python

	from ua2.otl import OneTimeLink

	link = OneTimeLink.create(resolve_name='django-url-name', resolve_kwargs={'value': 1})
	link.save(expire=3600)


Example with callback and authorization:

.. code-block:: python

	from ua2.otl import OntTimeLink

	def auth_callback(request, user_email):
	    user = get_object_or_404(User,
                                 email=user_email)
	    login(request, user)

    @login_required
	def password_restore(request):
		....

	def send_restore_passwortd(request):
		link = OneTimeLink.create(resolve_name='url-password-reset')
		link['user_email'] = request.POST.get('user_email')

		link.save(callback=auth_callback,
				  expire=3600,
				  count=1)

		return HttpResponse("http://127.0.0.1:8000%s" % link.url)
