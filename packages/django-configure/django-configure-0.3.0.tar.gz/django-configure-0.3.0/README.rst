=============
Django-Config
=============

(Works with django>=1.9, and possibly lower versions, but it wasn't tested, use at your own discretion)

This is a simple library which was build out of personal necessity.

As good as django is as a framework, it does not provide any 'out of the box' plugin for
extending settings.py with end user config files. Just to make sure - I do not treat python files as 
settings - giving end user ability to run arbitrary code in the application context is a great
way to bring disaster to whole system.

On the other hand settings.py contains a lot of code and settings which are not really up
for configuration (middleware, installed apps, this is clearly for the developer).

For a couple of smaller and larger projects now I had to manually write some code which was
responsible for reading external config files (usually `.ini` style) and inserting them into
settings.py, in some cases also some code for generating stub configs was required.

So at some point I decided - "Why shouldn't I make this into a reusable app?" - and this is how
this library was made.


The main purpose of this library is to let you specify end user config in a declarative way: ::

    config = django_configure.define({
        'Common': {
            'secret': django_configure.type.String('Secret for the application', default=generate_secret()),
            'static_root': django_configure.type.Path('Static root path (static files will be copied here)',
                                                   default='/var/lib/myapp/static/'),
            'static_url': django_configure.type.Path('Url to static files', default='/static/'),
            'media_root': django_configure.type.Path('Media root path (media files will be stored here)',
                                                  default='/var/lib/myapp/media/'),
            'media_url': django_configure.type.Path('Url to media files', '/media/'),
            'debug': django_configure.type.Boolean(help='if true debug mode will be enabled for the application, do not switch this in production', default=False)
        },
        'Database': {
            'url': django_configure.type.Database('Url to access database (including credentials)',
                                               default='sqlite:////var/lib/myapp/myapp.sqlite')
        }
    }, env_prefix='MYAPP')


Afterwards you can assign values to settings variables as follows: ::

    SECRET_KEY=config.get('Common.secret')

As the fields in the config file are type aware they do a good job at converting string to booleans, or numbers::

    DEBUG=config.get('Common.debug')


For convenience sake function for generating default config: ::

    config = django_configure.default('myapp', env_prefix='MYAPP')


Above code will generate config object with following fields (secret will be auto generated): ::

    {
        'Common': {
            'secret': django_configure.type.String('Secret for the application', default=generate_secret()),
            'static_root': django_configure.type.Path('Static root path (static files will be copied here)',
                                                   default='/var/lib/' + app_name + '/static/'),
            'static_url': django_configure.type.Path('Url to static files', default='/static/'),
            'media_root': django_configure.type.Path('Media root path (media files will be stored here)',
                                                  default='/var/lib/' + app_name + '/media/'),
            'media_url': django_configure.type.Path('Url to media files', '/media/'),
            'debug': django_configure.type.Boolean(help='if true debug mode will be enabled for the application, do not switch this in production', default=False)
        },
        'Database': {
            'url': django_configure.type.Database('Url to access database (including credentials)',
                                               default='sqlite:////var/lib/'+app_name+'/'+app_name+'.sqlite')
        }
    }


You can redefine / append parts of this via `config.append(additional_field)`: ::

    config = django_configure.default('myapp', env_prefix='MYAPP')
    config.append({'Common': {'media_root': '/my/secret/storage'}})


Config specified as follows can be read from environmental variable (env_prefix+CONFIG, in the case
of above code it will be MYAPP_CONFIG). Config path can also be specified in config definition via
`default_path` variable, but it's not recomended, as it hardcodes path into settings.py which is 
preciusly what we want to avoid.

After defining config in `settings.py` there is a possibility to generate template config and wsgi file
by running `manage.py` command: ::

    python manage.py createconfig <config_path> <wsgi_path>


Path to the config file will be hardcoded into wsgi file, so be mindful (You can always manually edit
wsgi file later)


Changelog
---------

* **Version 0.3.0**: Added support for python 3+, added `hostname` to config defaults