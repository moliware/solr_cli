solr_cli
========

Command line client for solr. Check full documentation here_


Installation
------------

From source code: ::

  python setup.py install

From pypi: ::

  pip install solr_cli


Usage
-----

Execute command line tool

::

  $ solr_cli
  (disconnected)$


Connect to a solr instance::

  (disconnected)$ connect http://localhost:8983/solr/
  (http://localhost:8983/solr/)$


Make a query::

  (http://localhost:8983/solr/)$ query *:*

  {
    "responseHeader": {
        "status": 0, 
        "QTime": 1, 
        "params": {
            "q": "*:*", 
            "wt": "python"
        }
    }, 
    "response": {
        "start": 0, 
        "numFound": 2961305, 
        "docs": [
            {......}
        ]
    }
  }

Make a query using http parameters::

  (http://localhost:8983/solr/)$ uri q=*:*&rows=0
  {
      "responseHeader": {
          "status": 0, 
          "QTime": 1, 
          "params": {
              "q": "*:*", 
              "rows": "0", 
              "wt": "python"
          }
      }, 
      "response": {
          "start": 0, 
          "numFound": 2961474, 
          "docs": []
      }
  }


.. _here: http://solr_cli.readthedocs.org