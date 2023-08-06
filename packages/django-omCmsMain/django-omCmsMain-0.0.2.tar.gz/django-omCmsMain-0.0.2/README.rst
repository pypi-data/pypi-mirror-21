Open Minds CMS 
==============

Open Minds CMS - Content Management System

Simple CMS built in Python Django
It is aimed to quick deploy a website, using BootStrap and Material Design Light, with a minimal templating capabilities.

It still an ongoing project.

Please check the Docs: http://omcmsdocs.readthedocs.io/


Quick start
-----------

If you are impatient like me, itching to see something making noise and somke, you can take this quick run! ;-)

1. Create a new Django Project
It is higly recomended that you use virtualenv to encapsulate it - https://virtualenv.pypa.io/

django-admin startproject [yourProjectName]

2. In [yourProjectName]/settings.py, add "omCmsMain" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'omCmsMain',
    ]

3. Edit [yourProjectName]/urls.py and make this changes:
3.1 Import include:
    from django.conf.urls import url, include

3.2 Include the omCmsMain URLconf in your project urls.py **AFTER** admin URLs, like this:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^', include('omCmsMain.urls')),
        ]

4. Run `python manage.py migrate` to create the omCmsMain models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to add content to your site.

6. Visit http://127.0.0.1:8000/ to see omCmsMain content.
