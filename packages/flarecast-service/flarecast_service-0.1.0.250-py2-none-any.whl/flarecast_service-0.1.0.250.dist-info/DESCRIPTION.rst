Flarecast Service
=================

Flarecast Service is the base package of all flarecast connexion
services.

|Latest Version| |Development Status| |Python Versions|

Idea
----

The Flarecast Service package provides support for
`connexion <https://github.com/zalando/connexion>`__ webservice
applications and includes following enhancements:

-  connexion application creation
-  automatic logging configuration
-  direct\_passthrough support
-  force\_type support
-  minified json encoder
-  automatic gzip compression
-  cors support
-  global exception handler

Usage
-----

Install
~~~~~~~

You just have to install the pip package.

.. code:: bash

    pip install flarecast-service

Example
~~~~~~~

Initialize a new ``FlarecastService`` and give it a name.

.. code:: python

    # create flarecast service
    service = FlarecastService('Property Service')

Create the service with the connexion parameters. This mehtod takes
``**kwargs``.

.. code:: python

    service.create(port=8002,
                   specification_dir=spec_dir)

Add **swagger configurations** to the blueprint.

.. code:: python

    # add yaml files
    service.app.add_api('propertyservice.yaml')
    service.app.add_api('query_builder.yaml', swagger_ui=False)

Publish the flask app as ``application`` for
\ `uwsgi <https://uwsgi-docs.readthedocs.org/en/latest/>`__ support.

.. code:: python

    # publish uwsgi flask app variable
    application = service.app.app

Run the connexion app if it has been started from the command line.

.. code:: python

    if __name__ == '__main__':
        service.run()

About
-----

*Implemented by Florian Bruggisser @ i4Ds 2016*

.. |Latest Version| image:: https://img.shields.io/pypi/v/flarecast-service.svg
   :target: https://pypi.python.org/pypi?:action=display&name=flarecast-service
.. |Development Status| image:: https://img.shields.io/pypi/status/flarecast-service.svg
   :target: https://dev.flarecast.eu/stash/projects/INFRA/repos/flarecastservice/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flarecast-service.svg
   :target: https://dev.flarecast.eu/stash/projects/INFRA/repos/flarecastservice/


