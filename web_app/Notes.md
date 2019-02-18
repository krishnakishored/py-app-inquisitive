#### Run the flask app

The `FLASK_APP` environment variable is the name of the module to import at flask run.

`$ export FLASK_APP=hello.py`
Error: Could not locate a Flask application.
You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.

*The most common reason is a typo or because you did not actually create an app object.*


`$ flask run`
or  `$ python -m flask run `
    * Running on http://127.0.0.1:5000/

#### Externally Visible Server
If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:
This tells your operating system to listen on all public IPs.

`$ flask run --host=0.0.0.0`


#### Debug Mode
 If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

To enable all development features (including debug mode) you can export the `FLASK_ENV` environment variable and set it to development before running the server:

`$ export FLASK_ENV=development`
`$ flask run`


This does the following things:
- it activates the debugger
- it activates the automatic reloader
- it enables the debug mode on the Flask application.
You can also control debug mode separately from the environment by exporting `FLASK_DEBUG=1`

* Install `python-dotenv` package  & Then you can just write the environment variable name and value in a .flaskenv file in the top-level directory of the project:
`FLASK_APP=wortspiel.py`


#### Routing
Use the route() decorator to bind a function to a URL.
You can make parts of the URL dynamic and attach multiple rules to a function.

* Variable Rules
You can add variable sections to a URL by marking sections with <variable_name>. Your function then receives the <variable_name> as a keyword argument. Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>.

Converter types:
string - (default) accepts any text without a slash
int - 	accepts positive integers
float - accepts positive floating point values
path - 	like string but also accepts slashes
uuid - 	accepts UUID strings

#### Unique URLs / Redirection Behavior
`@app.route('/projects/')`
The canonical URL for the projects endpoint has a trailing slash. It’s similar to a folder in a file system. If you access the URL _without_ a trailing slash, Flask redirects you to the canonical URL with the trailing slash.

`@app.route('/about')`
The canonical URL for the about endpoint does not have a trailing slash. It’s similar to the pathname of a file. Accessing the URL with a trailing slash produces a 404 “Not Found” error. This helps keep URLs unique for these resources, which helps search engines avoid indexing the same page twice.

#### URL Building
To build a URL to a specific function, use the `url_for()` function. It accepts the name of the function as its first argument and any number of keyword arguments, each corresponding to a variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters.
*from flask import url_for*

 - Reversing is often more descriptive than hard-coding the URLs.
 - You can change your URLs in one go instead of needing to remember to manually change hard-coded URLs.
 - URL building handles escaping of special characters and Unicode data transparently.
 - The generated paths are always absolute, avoiding unexpected behavior of relative paths in browsers.
 - If your application is placed outside the URL root, for example, in */myapplication* instead of */*, url_for() properly handles that for you.

#### HTTP Methods
By default, a route only answers to GET requests. You can use the `methods` argument of the route() decorator to handle different HTTP methods.
_from flask import request_

If GET is present, Flask automatically adds support for the HEAD method and handles HEAD requests according to the HTTP RFC. Likewise, OPTIONS is automatically implemented for you.


#### Static Files

Dynamic web applications also need static files. During development Flask can do that as well. Just create a folder called static in your package or next to your module and it will be available at /static on the application.

To generate URLs for static files, use the special 'static' endpoint name:
`url_for('static', filename='style.css')`  - The file has to be stored on the filesystem as static/style.css.

#### Rendering Templates
To render a template you can use the `render_template()` method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments.
Flask will look for templates in the templates folder. So if your application is a module, this folder is next to that module, if it’s a package it’s actually inside your package:

Inside templates you also have access to the `request`, `session` and `g`  objects (It’s something in which you can store information for your own needs) as well as the `get_flashed_messages()` function.

Templates are especially useful if inheritance is used.  It makes it possible to keep certain elements on each page (like header, navigation and footer).

Automatic escaping is enabled, so if `name` contains HTML it will be escaped automatically. If you can trust a variable and you know that it will be safe HTML (for example because it came from a module that converts wiki markup to HTML) you can mark it as safe by using the `Markup` class or by using the `|safe` filter in the template

#### Accessing Request Data
For web applications it’s crucial to react to the data a client sends to the server. In Flask this information is provided by the global request object. If you have some experience with Python you might be wondering how that object can be global and how Flask manages to still be threadsafe. The answer is `context locals`:
Certain objects in Flask are global objects, but not of the usual kind. *These objects are actually proxies to objects that are local to a specific context.*

Imagine the context being the handling thread. A request comes in and the web server decides to spawn a new thread (or something else, the underlying object is capable of dealing with concurrency systems other than threads). When Flask starts its internal request handling it figures out that the current thread is the active context and binds the current application and the WSGI environments to that context (thread). It does that in an intelligent way so that one application can invoke another application without breaking.

Basically you can completely ignore that this is the case unless you are doing something like unit testing. You will notice that code which depends on a request object will suddenly break because there is no request object. *The solution is creating a request object yourself and binding it to the context.* The easiest solution for unit testing is to use the `test_request_context()` context manager. In combination with the with statement it will bind a test request so that you can interact with it.

*The other possibility is passing a whole WSGI environment to the request_context() method*

#### The Request Object
The current request method is available by using the `method` attribute. To access form data (data transmitted in a `POST` or `PUT` request) you can use the `form` attribute.

What happens if the key does not exist in the form attribute? In that case a special `KeyError` is raised. You can catch it like a standard KeyError but if you don’t do that, a HTTP 400 Bad Request error page is shown instead.

To access parameters submitted in the URL (`?key=value`) you can use the `args` attribute: `searchword = request.args.get('key', '')`

#### File Uploads
You can handle uploaded files with Flask easily. Just make sure not to forget to set the `enctype="multipart/form-data"` attribute on your HTML form, otherwise the browser will not transmit your files at all.


Uploaded files are stored in memory or at a temporary location on the filesystem. You can access those files by looking at the `files` attribute on the request object. Each uploaded file is stored in that dictionary. It behaves just like a standard Python `file` object, but it also has a `save()` method that allows you to store that file on the filesystem of the server.
If you want to use the filename of the client to store the file on the server, pass it through the `secure_filename()` function that `Werkzeug` provides for you:


#### Cookies
To access cookies you can use the `cookies` attribute. To set cookies you can use the `set_cookie` method of response objects. The `cookies` attribute of request objects is a dictionary with all the cookies the client transmits. If you want to use sessions, do not use the cookies directly but instead use the `Sessions` in Flask that add some security on top of cookies for you.

Note that cookies are set on response objects. Since you normally just return strings from the view functions Flask will convert them into response objects for you. If you explicitly want to do that you can use the `make_response()` function and then modify it.

This is possible by utilizing the `Deferred Request Callbacks` pattern.

#### Redirects and Errors
To redirect a user to another endpoint, use the `redirect()` function; to abort a request early with an error code, use the `abort()` function:

By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the `errorhandler()` decorator: `@app.errorhandler(404)`
`return render_template('page_not_found.html'), 404` - Note the 404 after the render_template() call. This tells Flask that the status code of that page should be 404 which means not found. By default 200 is assumed which translates to: all went well.

#### About Responses
The return value from a view function is automatically converted into a `response` object for you.

* If a response object of the correct type is returned it’s directly returned from the view.
* If it’s a string, a response object is created with that data and the default parameters.
* If a tuple is returned the items in the tuple can provide extra information. Such tuples have to be in the form `(response, status, headers)` or `(response, headers)`  where at least one item has to be in the tuple. The `status` value will override the status code and headers can be a list or dictionary of additional header values.
* If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.
* If you want to get hold of the resulting response object inside the view you can use the make_response() function.
* You just need to wrap the return expression with make_response() and get the response object to modify it, then return it:

#### Sessions

In addition to the request object there is also a second object called `session` which allows you to store information specific to a user from one request to the next. This is implemented on top of cookies for you and signs the cookies cryptographically. What this means is that the user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing. In order to use sessions you have to set a `secret key`.

The `escape()` mentioned here does escaping for you if you are not using the template engine (as in this example).

A note on cookie-based sessions: Flask will take the values you put into the session object and serialize them into a cookie. If you are finding some values do not persist across requests, cookies are indeed enabled, and you are not getting a clear error message, check the size of the cookie in your page responses compared to the size supported by web browsers.

Besides the default client-side based sessions, if you want to handle sessions on the server-side instead, there are several Flask extensions that support this.


#### Message Flashing
Flask provides a really simple way to give feedback to a user with the flashing system. The flashing system basically makes it possible to record a message at the end of a request and access it on the next (and only the next) request. This is usually combined with a layout template to expose the message.

To flash a message use the `flash()` method, to get hold of the messages you can use `get_flashed_messages()` which is also available in the templates.

#### Logging
The attached logger is a standard logging
app.logger.debug()
app.logger.warning()
app.logger.error()

#### Hooking in WSGI Middlewares
If you want to add a WSGI middleware to your application you can wrap the internal `WSGI` application.
`from werkzeug.contrib.fixers import LighttpdCGIRootFix`
`app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)`

#### Using Flask Extensions
Extensions are packages that help you accomplish common tasks.
`Flask-SQLAlchemy` provides SQLAlchemy support that makes it simple and easy to use with Flask.

#### Deploying to a Web Server


#### Folder Strucuture of web app
* `run.py`	This is the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development.
* `requirements.txt`	This file lists all of the Python packages that your app depends on. You may have separate files for production and development dependencies.
* `config.py`	This file contains most of the configuration variables that your app needs.
* `/instance/config.py`	This file contains configuration variables that shouldn’t be in version control. This includes things like API keys and database URIs containing passwords. This also contains variables that are specific to this particular instance of your application. For example, you might have DEBUG = False in config.py, but set DEBUG = True in instance/config.py on your local machine for development. Since this file will be read in after config.py, it will override it and set DEBUG = True.
* `/yourapp/`	This is the package that contains your application.
* `/yourapp/__init__.py`	This file initializes your application and brings together all of the various components.
*`/yourapp/views.py`	This is where the routes are defined. It may be split into a package of its own (yourapp/views/) with related views grouped together into modules.
* `/yourapp/models.py`	This is where you define the models of your application. This may be split into several modules in the same way as views.py.
* `/yourapp/static/`	This directory contains the public CSS, JavaScript, images and other files that you want to make public via your app. It is accessible from yourapp.com/static/ by default.
* `/yourapp/templates/`	This is where you’ll put the Jinja2 templates for your app.

