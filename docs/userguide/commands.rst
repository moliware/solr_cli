.. _commands:

Commands
========


Connecting to solr
------------------

connect
.......

.. program:: connect

.. option:: solr_url

    Url of the index you want to query.


Connects to a solr server located in solr_url. It doesn't open a real connection
it just checks if the server exits and is up.

Examples::

    connect http://localhost:8983/solr
    connect http://localhost:8983/solr/index_name

Querying to Solr
----------------

query
.....

.. program:: query

.. option:: q

    Value of the parameter 'q'.

Makes a simple query to a solr server. 

Examples::

    query *:*
    query type:"book" AND price:[* TO 10]

uri
...

.. program:: uri

.. option:: params

    Specify all the http parameters.

Makes a requests to a solr server allowing all http paramaters.
Paramenter 'q' must be specified.

Example::

    uri q=*:*&facet=true&facet.field=price&rows=0


General operations
------------------

ping
....

Checks if the solr server is up. 'OK' is printed if so.


commit
......

Sends a commit to the solr server.

optimize
........

Sends optimize operation to solr server.

quit
....

Exit



