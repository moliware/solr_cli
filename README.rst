solr-cli
========

Command line client for solr


Installation
------------

From source code: ::

  python setup.py install

From pypi: ::

  pip install solr_cli


Usage
-----
::

  $ solr_cli
  
  (disconnected)$ connect http://localhost:8983/solr/
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