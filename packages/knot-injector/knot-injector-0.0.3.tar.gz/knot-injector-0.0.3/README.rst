Knot Injector
========

Framework agnostic dependency injections

This library build as a wrapper for `Knot`_ Dependencies Container.


Installation
------------

``pip install knot-injector``

Usage
-----

Example:

.. code:: python

    import sqlalchemy as db
    from sqlalchemy.orm import sessionmaker

    from knot_injector import Container

    registry = Container()

    settings = {
        'db': {
            'uri': 'sqlite://',
            'echo': False,
            'encoding': 'utf8',
        },
    }

    registry.add_service(lambda _: settings, name='settings')

    @registry.service()
    def dbengine(container, settings):
        uri = settings['db']['uri']
        return create_engine(uri, **settings['db'])

    @registry.factory(name='dbsession')
    def database_session(container, dbengine):
        session = sessionmaker()
        session.configure(bind=dbengine)
        return session()


    class ItemResource(object):

        @registry.inject
        def on_get(request, response, item_id, dbsession):
            response.data = dbsession.query(Item).filter(Item.id == item_id).one()


.. _Knot: https://github.com/jaapverloop/knot
