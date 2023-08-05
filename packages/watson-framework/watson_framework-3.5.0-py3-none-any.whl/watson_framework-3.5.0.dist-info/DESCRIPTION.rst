contributors including:

	- Simon Coulton <simon@bespohk.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Description: Watson-Framework
        ================
        
        ::
        
            It's elementary my dear Watson
        
        Watson is an easy to use framework designed to get out of your way and
        let you code your application rather than wrangle with the framework.
        
        For full documentation please see `Read The
        Docs <http://watson-framework.readthedocs.org/>`__.
        
        Build Status
        ^^^^^^^^^^^^
        
        |Build Status| |Coverage Status| |Version|
        
        Installation
        ------------
        
        ``pip install watson-framework``
        
        Dependencies
        ------------
        
        -  watson-cache
        -  watson-common
        -  watson-console
        -  watson-di
        -  watson-dev
        -  watson-events
        -  watson-filter
        -  watson-form
        -  watson-html
        -  watson-http
        -  watson-routing
        -  watson-validators
        
        Benchmarks
        ----------
        
        Using falcon-bench, Watson received the following requests per second (Django and Flask supplied for comparative purposes).
        
        1. watson.........11,920 req/sec or 83.89 ms/req  (3x)
        2. django..........7,696 req/sec or 129.94 ms/req (2x)
        3. flask...........4,281 req/sec or 233.58 ms/req (1x)
        
        .. |Build Status| image:: https://img.shields.io/travis/watsonpy/watson-framework.svg?maxAge=2592000
           :target: https://travis-ci.org/watsonpy/watson-framework
        .. |Coverage Status| image:: https://img.shields.io/coveralls/watsonpy/watson-framework.svg?maxAge=2592000
           :target: https://coveralls.io/r/watsonpy/watson-framework
        .. |Version| image:: https://img.shields.io/pypi/v/watson-framework.svg?maxAge=2592000
           :target: https://pypi.python.org/pypi/watson-framework/
        
Keywords: watson,python3,web framework,framework,wsgi,web
Platform: Python 3.3
Classifier: Development Status :: 5 - Production/Stable
Classifier: Environment :: Web Environment
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Topic :: Internet :: WWW/HTTP
Classifier: Topic :: Internet :: WWW/HTTP :: Dynamic Content
Classifier: Topic :: Internet :: WWW/HTTP :: WSGI
Classifier: Topic :: Internet :: WWW/HTTP :: WSGI :: Application
Classifier: Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware
Classifier: Topic :: Internet :: WWW/HTTP :: WSGI :: Server
