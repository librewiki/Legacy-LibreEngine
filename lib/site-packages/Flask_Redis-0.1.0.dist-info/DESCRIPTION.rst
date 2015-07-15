   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
Download-URL: https://github.com/underyx/flask-redis/releases
Description: Flask-Redis
        ===========
        
        
        .. image:: https://travis-ci.org/rhyselsmore/flask-redis.png?branch=master
                :target: https://travis-ci.org/rhyselsmore/flask-redis
        
        .. image:: https://pypip.in/d/Flask-Redis/badge.png
                :target: https://crate.io/packages/Flask-Redis/
        
        Add Redis Support to Flask.
        
        Built on top of `redis-py <https://github.com/andymccurdy/redis-py>`_.
        
        
        Contributors
        ------------
        
        - Rhys Elsmore - @rhyselsmore - https://github.com/rhyselsmore
        - Bence Nagy - @underyx - https://github.com/underyx
        - Lars Schöning - @lyschoening - https://github.com/lyschoening
        - Aaron Tygart - @thekuffs - https://github.com/thekuffs
        - Christian Sueiras - @csueiras - https://github.com/csueiras
        
        
        Installation
        ------------
        
        .. code-block:: bash
        
            pip install flask-redis
        
        Or if you *must* use easy_install:
        
        .. code-block:: bash
        
            alias easy_install="pip install $1"
            easy_install flask-redis
        
        
        Configuration
        -------------
        
        Your configuration should be declared within your Flask config. You can declare
        via a Redis URL containing the database
        
        .. code-block:: python
        
            REDIS_URL = "redis://:password@localhost:6379/0"
        
        
        To create the redis instance within your application
        
        .. code-block:: python
        
            from flask import Flask
            from flask.ext.redis import FlaskRedis
        
            app = Flask(__name__)
            redis_store = FlaskRedis(app)
        
        or
        
        .. code-block:: python
        
            from flask import Flask
            from flask.ext.redis import FlaskRedis
        
            redis_store = FlaskRedis()
        
            def create_app():
                app = Flask(__name__)
                redis_store.init_app(app)
                return app
        
        or perhaps you want to use ``StrictRedis``
        
        .. code-block:: python
        
            from flask import Flask
            from flask.ext.redis import FlaskRedis
            from redis import StrictRedis
        
            app = Flask(__name__)
            redis_store = FlaskRedis.from_custom_provider(StrictRedis, app)
        
        or maybe you want to use
        `mockredis <https://github.com/locationlabs/mockredis>`_ to make your unit
        tests simpler.  As of ``mockredis`` 2.9.0.10, it does not have the ``from_url()``
        classmethod that ``FlaskRedis`` depends on, so we wrap it and add our own.
        
        .. code-block:: python
        
        
            from flask import Flask
            from flask.ext.redis import FlaskRedis
            from mockredis import MockRedis
        
        
        
            class MockRedisWrapper(MockRedis):
                '''A wrapper to add the `from_url` classmethod'''
                @classmethod
                def from_url(cls, *args, **kwargs):
                    return cls()
        
            def create_app():
                app = Flask(__name__)
                if app.testing:
                    redis_store = FlaskRedis.from_custom_provider(MockRedisWrapper)
                else:
                    redis_store = FlaskRedis()
                redis_store.init_app(app)
                return app
        
        Usage
        -----
        
        ``FlaskRedis`` proxies attribute access to an underlying Redis connection. So treat it as if it were a regular ``Redis`` instance.
        
        .. code-block:: python
        
            from core import redis_store
        
            @app.route('/')
            def index():
                return redis_store.get('potato', 'Not Set')
        
        **Protip:** The `redis-py <https://github.com/andymccurdy/redis-py>`_ package currently holds the 'redis' namespace,
        so if you are looking to make use of it, your Redis object shouldn't be named 'redis'.
        
        For detailed instructions regarding the usage of the client, check the `redis-py <https://github.com/andymccurdy/redis-py>`_ documentation.
        
        Advanced features, such as Lua scripting, pipelines and callbacks are detailed within the projects README.
        
        Contribute
        ----------
        
        #. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a Contributor Friendly tag for issues that should be ideal for people who are not very familiar with the codebase yet.
        #. Fork `the repository`_ on Github to start making your changes to the **master** branch (or branch off of it).
        #. Write a test which shows that the bug was fixed or that the feature works as expected.
        #. Send a pull request and bug the maintainer until it gets merged and published.
        
        .. _`the repository`: http://github.com/rhyselsmore/flask-redis
        
        
        History
        =======
        
        0.1.0 (4/15/2015)
        -----------------
        
        - **Deprecation:** Renamed ``flask_redis.Redis`` to ``flask_redis.FlaskRedis``.
          Using the old name still works, but emits a deprecation warning, as it will
          be removed from the next version
        - **Deprecation:** Setting a ``REDIS_DATABASE`` (or equivalent) now emits a
          depracation warning as it will be removed in the version in favor of
          including the database number in ``REDIS_URL`` (or equivalent)
        - Added a ``FlaskRedis.from_custom_provider(provider)`` class method for using
          any redis provider class that supports instantiation with a ``from_url``
          class method
        - Added a ``strict`` parameter to ``FlaskRedis`` which expects a boolean value
          and allows choosing between using ``redis.StrictRedis`` and ``redis.Redis``
          as the defualt provider.
        - Made ``FlaskRedis`` register as a Flask extension through Flask's extension
          API
        - Rewrote test suite in py.test
        - Got rid of the hacky attribute copying mechanism in favor of using the
          ``__getattr__`` magic method to pass calls to the underlying client
        
        0.0.6 (4/9/2014)
        ----------------
        
        - Improved Python 3 Support (Thanks underyx!).
        - Improved test cases.
        - Improved configuration.
        - Fixed up documentation.
        - Removed un-used imports (Thanks underyx and lyschoening!).
        
        
        0.0.5 (17/2/2014)
        ----------------
        
        - Improved support for the config prefix.
        
        0.0.4 (17/2/2014)
        ----------------
        
        - Added support for config_prefix, allowing multiple DBs.
        
        0.0.3 (6/7/2013)
        ----------------
        
        - Added TravisCI Testing for Flask 0.9/0.10.
        - Added Badges to README.
        
        0.0.2 (6/7/2013)
        ----------------
        
        - Implemented a very simple test.
        - Fixed some documentation issues.
        - Included requirements.txt for testing.
        - Included task file including some basic methods for tests.
        
        0.0.1 (5/7/2013)
        ----------------
        
        - Conception
        - Initial Commit of Package to GitHub.
        
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Web Environment
Classifier: Framework :: Flask
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: Apache Software License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.4
Classifier: Topic :: Internet :: WWW/HTTP :: Dynamic Content
Classifier: Topic :: Software Development :: Libraries :: Python Modules
