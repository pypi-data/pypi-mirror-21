Basics
------

::

    # This is a comment. Normal Python syntax.
    if path == '/hello':
        header('Content-Type', 'text/plain')
        body('Hello world!\r\n')
    else:
        error(404)


“RESTful” routing
-----------------

::

    if route('/v1/products/:product_id'):
        if GET or HEAD:
            json({'id': int(product_id),
                  'inStock': True})
        elif PUT:
            # Pretend that we saved it
            json(request.json)
        elif DELETE:
            status(204)   # No Content


HTML pages
----------

To get a simple page::

    html()

If you want to change the contents of the page, the full `Dominate`_ library
is at your service (``dominate.tags`` imported as ``H``)::

    with html():
        H.h1('Welcome to our site')
        H.p('Have a look at our ',
            H.a('products', href='/products'))

To change the ``<head>``::

    with html() as document:
        with document.head:
            H.style('h1 {color: red}')
        H.h1('Welcome to our site')

.. _Dominate: https://github.com/Knio/dominate


Request details
---------------

::

    if request.json:     # parsed JSON body
        name = request.json['name']
    elif request.form:   # URL-encoded or multipart
        name = request.form['name']
    elif query:     # query string parameters
        name = query['name']
    else:
        raw_name = request.body     # raw bytes
        name = raw_name.decode('utf-8')

    # Header names are case-insensitive
    if 'json' in request.headers['Accept']:
        json({'hello': name})
    else:
        text('Hello %s!\r\n' % name)


Response headers
----------------

``header()`` *replaces* the given header, so this will send
**only** ``max-age``::

    header('Cache-Control', 'public')
    header('Cache-Control', 'max-age=3600')

To *add* a header instead::

    add_header('Set-Cookie', 'sessionid=123456')
    add_header('Set-Cookie', '__adtrack=abcdef')


Custom status code and reason
-----------------------------

::

    status(567, 'Server Fell Over')
    text('Server crashed, sorry!\r\n')


Redirection
-----------

::

    if path == '/':
        redirect('/index.html')
    elif path == '/index.html':
        html()

``redirect()`` sends `302 (Found)`_ by default, but you can override::

    redirect('/index.html', 307)

.. _302 (Found): https://tools.ietf.org/html/rfc7231#section-6.4.3


Authentication
--------------

To demand `basic`_ authentication::

    basic_auth()
    with html():
        H.h1('Super-secret page!')

This sends `401 (Unauthorized)`_ unless the request had ``Authorization``
with the ``Basic`` scheme (credentials are ignored).

Similarly for `digest`_::

    digest_auth()

And for `bearer`_::

    bearer_auth()

.. _basic: https://en.wikipedia.org/wiki/Basic_access_authentication
.. _401 (Unauthorized): https://tools.ietf.org/html/rfc7235#section-3.1
.. _digest: https://en.wikipedia.org/wiki/Digest_access_authentication
.. _bearer: https://tools.ietf.org/html/rfc6750


Body from file
--------------

::

    text(open('/etc/services'))


Inspecting requests
-------------------

To see what the client sends, including headers (but not the raw body),
put ``debug()`` somewhere early in your rules::

    debug()

and watch the console output. Alternatively, for even more diagnostics,
run Turq with the ``--verbose`` option.

Or `use mitmproxy`_.

.. _use mitmproxy:
   http://turq.readthedocs.io/en/stable/guide.html#using-mitmproxy-with-turq


Forwarding requests
-------------------

Turq can act as a gateway or “reverse proxy”::

    forward('httpbin.org', 80,  # host, port
            target)             # path + query string
    # At this point, response from httpbin.org:80
    # has been copied to Turq, and can be tweaked:
    delete_header('Server')
    add_header('Cache-Control', 'max-age=86400')

Turq uses TLS when connecting to port 443, but **ignores certificates**.
You can override TLS like this::

    forward('develop1.example', 8765,
            '/v1/articles', tls=True)


Cross-origin resource sharing
-----------------------------

``cors()`` adds the right ``Access-Control-*`` headers, and handles
preflight requests automatically::

    cors()
    json({'some': 'data'})

For legacy systems, JSONP is also supported, reacting automatically
to a ``callback`` query parameter::

    json({'some': 'data'}, jsonp=True)


Compression
-----------

Call ``gzip()`` after setting the body::

    with html():
        # 100 paragraphs of text
        for i in range(100):
            H.p(lorem_ipsum())
    gzip()


Random responses
----------------

::

    if maybe(0.1):    # 10% probability
        error(503)
    else:
        html()


Response framing
----------------

By default, if the client supports it, Turq uses ``Transfer-Encoding: chunked``
and keeps the connection alive.

To use ``Content-Length`` instead of ``Transfer-Encoding``,
call ``content_length()`` after you’ve set the body::

    text('Hello world!\r\n')
    content_length()

To close the connection after sending the response::

    add_header('Connection', 'close')
    text('Hello world!\r\n')


Streaming responses
-------------------

::

    header('Content-Type', 'text/event-stream')
    sleep(1)        # 1 second delay
    chunk('data: my event 1\r\n\r\n')
    sleep(1)
    chunk('data: my event 2\r\n\r\n')
    sleep(1)
    chunk('data: my event 3\r\n\r\n')

Once you call ``chunk()``, the response begins streaming.
Any headers you set after that will be sent in the `trailer part`_::

    header('Content-Type', 'text/plain')
    header('Trailer', 'Content-MD5')
    chunk('Hello, ')
    chunk('world!\n')
    header('Content-MD5', '746308829575e17c3331bbcb00c0898b')

.. _trailer part: https://tools.ietf.org/html/rfc7230#section-4.1.2


Handling ``Expect: 100-continue``
---------------------------------

::

    with interim():
        status(100)

    text('Resource updated OK')

In the above example, `100 (Continue)`_ is sent immediately after the
``interim()`` block, but the final 200 (OK) response is sent only after
reading the full request body.

If instead you want to send a response *before* reading the request body::

    error(403)      # Forbidden
    flush()

.. _100 (Continue): https://tools.ietf.org/html/rfc7231#section-6.2.1


Custom methods
--------------

::

    if method != 'FROBNICATE':
        error(405)   # Method Not Allowed
        header('Allow', 'FROBNICATE')


Switching protocols
-------------------

::

    if request.headers['Upgrade'] == 'QXTP':
        with interim():
            status(101)   # Switching Protocols
            header('Upgrade', 'QXTP')
            header('Connection', 'upgrade')
        send_raw('This is no longer HTTP!\r\n')
        send_raw('This is QXTP now!\r\n')


Anything else
-------------

In the end, Turq rules are just Python code that is not sandboxed,
so you can import and use anything you like. For example,
to send random binary data::

    import os
    header('Content-Type', 'application/octet-stream')
    body(os.urandom(128))
