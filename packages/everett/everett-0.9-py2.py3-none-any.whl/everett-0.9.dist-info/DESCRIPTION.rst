=======
Everett
=======

Everett is a configuration library.

:Code:          https://github.com/willkg/everett
:Issues:        https://github.com/willkg/everett/issues
:License:       MPL v2
:Documentation: https://everett.readthedocs.io/


Goals
=====

This library tries to do configuration with minimal "fanciness":

Configuration with Everett:

* is composeable and flexible
* makes it easier to provide helpful error messages for users trying to
  configure your software
* can pull configuration from a variety of specified sources (environment, ini
  files, dict, write-your-own)
* supports parsing values (bool, int, lists, ..., write-your-own)
* supports key namespaces
* facilitates writing tests that change configuration values
* supports component architectures with auto-documentation of configuration with
  a Sphinx ``autocomponent`` directive

Everett is inspired by `python-decouple
<https://github.com/henriquebastos/python-decouple>`_ and `configman
<https://configman.readthedocs.io/en/latest/>`_.


Why not other libs?
===================

Most other libraries I looked at had one or more of the following issues:

* were tied to a specific web app framework
* didn't allow you to specify configuration sources
* provided poor error messages when you configure things wrong
* had a global configuration object
* made it really hard to override specific configuration when writing tests
* had no facilities for auto-documenting configuration for components


Quick start
===========

Say you're writing a web app using some framework that doesn't provide
infrastructure for configuration.

You want to pull configuration from an INI file stored in a place specified by
``FOO_INI`` in the environment. You want to pull infrastructure values from the
environment. Values from the environment should override values from the INI
file.

First, you set up your ``ConfigManager`` in your webapp::

    from everett.manager import ConfigManager, ConfigOSEnv, ConfigIniEnv


    class MyWSGIApp(SomeFrameworkApp):
        def __init__(self):
            self.config = ConfigManager(
                # Specify one or more configuration environments in
                # the order they should be checked
                [
                    # Looks in OS environment first
                    ConfigOSEnv(),

                    # Looks in INI files in order specified
                    ConfigIniEnv([
                        os.environ.get('MYAPP_INI'),
                        '~/.myapp.ini',
                        '/etc/myapp.ini'
                    ]),
                ],

                # Make it easy for users to find your configuration
                # docs
                doc='Check https://example.com/configuration for docs'
            )

            # Set ``is_debug`` based on configuration
            self.is_debug = self.config('debug', parser=bool)


    def get_app():
        return MyWSGIApp()


Now all configuration for the app can be pulled from the ``.config`` property.

Let's write some tests that verify behavior based on the ``debug`` configuration
value::

    from everett.manager import config_override

    @config_override(DEBUG='true')
    def test_debug_true():
        app = get_app()
        ...

    @config_override(DEBUG='false')
    def test_debug_false():
        app = get_app()
        ...


This works with frameworks that do have configuration infrastructure like
Django and Flask.

This works with non-web things, too, like command line programs.

Everett supports components, too. Say your app needs to connect to RabbitMQ.
With Everett, you can wrap the configuration up with the component::

    from everett.component import RequiredConfigMixin, ConfigOptions

    class RabbitMQComponent(RequiredConfigMixin):
        required_config = ConfigOptions()
        required_config.add_option(
            'host',
            doc='RabbitMQ host to connect to'
        )
        required_config.add_option(
            'port',
            default='5672',
            doc='Port to use',
            parser=int
        )
        required_config.add_option(
            'queue_name',
            doc='Queue to insert things into'
        )

        def __init__(self, config):
            # Bind the configuration to just the configuration this
            # component requires such that this component is
            # self-contained.
            self.config = config.with_options(self)

            self.host = self.config('host')
            self.port = self.config('port')
            self.queue_name = self.config('queue_name')


Then instantiate a ``RabbitMQComponent``, but with configuration in the ``rmq``
namespace::

    queue = RabbitMQComponent(config.with_namespace('rmq'))


In your environment, you would provide ``RMQ_HOST``, etc for this component.

You can auto-document the configuration for this component in your Sphinx docs
with::

    .. autocomponent:: path.to.RabbitMQComponent


Say your app actually needs to connect to two separate queues--one for regular
processing and one for priority processing::

    regular_queue = RabbitMQComponent(
        config.with_namespace('regular').with_namespace('rmq')
    )
    priority_queue = RabbitMQComponent(
        config.with_namespace('priority').with_namespace('rmq')
    )


In your environment, you provide the regular queue configuration with
``RMQ_REGULAR_HOST``, etc and the priority queue configuration with
``RMQ_PRIORITY_HOST``, etc.

Same component code. Two different instances pulling configuration from two
different namespaces.

Components support subclassing, mixins and all that, too.


Install
=======

>From PyPI
---------

Run::

    $ pip install everett


For hacking
-----------

Run::

    # Clone the repository
    $ git clone https://github.com/willkg/everett

    # Create a virtualenvironment
    ...

    # Install Everett and dev requirements
    $ pip install -r requirements-dev.txt


History
=======

0.9 (April 7th, 2017)
---------------------

Changed:

* Rewrite Sphinx extension. The extension is now in the ``everett.sphinxext``
  module and the directive is now ``.. autocomponent::``. It generates better
  documentation and it now indexes Everett components and options.

  This is backwards-incompatible. You will need to update your Sphinx
  configuration and documentation.

* Changed the ``HISTORY.rst`` structure.

* Changed the repr for ``everett.NO_VALUE`` to ``"NO_VALUE"``.

* ``InvalidValueError`` and ``ConfigurationMissingError`` now have
  ``namespace``, ``key``, and ``parser`` attributes allowing you to build your
  own messages.

Fixed:

* Fix an example in the docs where the final key was backwards. Thank you, pjz!

Documentation fixes and updates.


0.8 (January 24th, 2017)
------------------------

Added:

* Add ``:namespace:`` and ``:case:`` arguments to autoconfig directive. These
  make it easier to cater your documentation to your project's needs.

* Add support for Python 3.6.

Minor documentation fixes and updates.


0.7 (January 5th, 2017)
-----------------------

Added:

* Feature: You can now include documentation hints and urls for
  ``ConfigManager`` objects and config options. This will make it easier for
  your users to debug configuration errors they're having with your software.

Fixed:

* Fix ``ListOf`` so it returns empty lists rather than a list with a single
  empty string.

Documentation fixes and updates.


0.6 (November 28th, 2016)
-------------------------

Added:

* Add ``RequiredConfigMixin.get_runtime_config()`` which returns the runtime
  configuration for a component or tree of components. This lets you print
  runtime configuration at startup, generate INI files, etc.

* Add ``ConfigObjEnv`` which lets you use an object for configuration. This
  works with argparse's Namespace amongst other things.

Changed:

* Change ``:show-docstring:`` to take an optional value which is the attribute
  to pull docstring content from. This means you don't have to mix programming
  documentation with user documentation--they can be in different attributes.

* Improve configuration-related exceptions. With Python 3, configuration errors
  all derive from ``ConfigurationError`` and have helpful error messages that
  should make it clear what's wrong with the configuration value. With Python 2,
  you can get other kinds of Exceptions thrown depending on the parser used, but
  configuration error messages should still be helpful.

Documentation fixes and updates.


0.5 (November 8th, 2016)
------------------------

Added:

* Add ``:show-docstring:`` flag to ``autoconfig`` directive.

* Add ``:hide-classname:`` flag to ``autoconfig`` directive.

Changed:

* Rewrite ``ConfigIniEnv`` to use configobj which allows for nested sections in
  INI files. This also allows you to specify multiple INI files and have later
  ones override earlier ones.

Fixed:

* Fix ``autoconfig`` Sphinx directive and add tests--it was all kinds of broken.

Documentation fixes and updates.


0.4 (October 27th, 2016)
------------------------

Added:

* Add ``raw_value`` argument to config calls. This makes it easier to write code
  that prints configuration.

Fixed:

* Fix ``listify(None)`` to return ``[]``.

Documentation fixes and updates.


0.3.1 (October 12th, 2016)
--------------------------

Fixed:

* Fix ``alternate_keys`` with components. Previously it worked for everything
  but components. Now it works with components, too.

Documentation fixes and updates.


0.3 (October 6th, 2016)
-----------------------

Added:

* Add ``ConfigManager.from_dict()`` shorthand for building configuration
  instances.

* Add ``.get_namespace()`` to ``ConfigManager`` and friends for getting
  the complete namespace for a given config instance as a list of strings.

* Add ``alternate_keys`` to config call. This lets you specify a list of keys in
  order to try if the primary key doesn't find a value. This is helpful for
  deprecating keys that you used to use in a backwards-compatible way.

* Add ``root:`` prefix to keys allowing you to look outside of the current
  namespace and at the configuration root for configuration values.

Changed:

* Make ``ConfigDictEnv`` case-insensitive to keys and namespaces.

Documentation fixes and updates.


0.2 (August 16th, 2016)
-----------------------

Added:

* Add ``ConfigEnvFileEnv`` for supporting ``.env`` files. Thank you, Paul!

* Add "on" and "off" as valid boolean values. This makes it easier to use config
  for feature flippers. Thank you, Paul!

Changed:

* Change ``ConfigIniEnv`` to take a single path or list of paths. Thank you,
  Paul!

* Make ``NO_VALUE`` falsy.

Fixed:

* Fix ``__call__`` returning None--it should return ``NO_VALUE``.

Lots of docs updates: finished the section about making your own parsers, added
a section on using dj-database-url, added a section on django-cache-url and
expanded on existing examples.


0.1 (August 1st, 2016)
----------------------

Initial writing.


