#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
solr_cli
~~~~~~~~

Command line client for solr. 

"""
import cmd
import json
import mysolr

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JavascriptLexer
from urlparse import parse_qs


__version__ = '0.1'

 
class SolrCLI(cmd.Cmd):
    """ """

    def __init__(self):
        # Old style class :\
        cmd.Cmd.__init__(self)
        self.solr = None
        self.prompt = '(disconnected)$ '

    def do_connect(self, host):
        """connect <solr_url>

        connects to a solr server located in solr_url. Example:

        connect http://localhost:8983/solr
        """
        self.solr = mysolr.Solr(host)
        if self.solr.is_up():
            self.prompt = '(%s)$ ' % host
        else:
            print 'Cant\'t connect to %s' % host

    def do_ping(self, line):
        """ping

        checks if the solr server is up
        """
        if self.solr.is_up():
            print 'OK'
        else:
            print 'Cant\'t connect to %s' % host

    def do_query(self, query):
        """query <q>

        makes a query to a solr server. Examples:

        query *:*
        query type:"book" AND price:[* TO 10]
        """
        response = self.solr.search(q=query)
        if response.status == 200:
            print self.__highlight(response.raw_content)
        else:
            print response.message

    def do_uri(self, uri):
        """uri <uri>

        makes a requests to a solr server allowing all paramaters. Example:

        uri q=*:*&facet=true&facet.field=price&rows=0
        """
        response = self.solr.search(**parse_qs(uri))
        if response.status == 200:
            print type(response.raw_content)
            print self.__highlight(response.raw_content)
        else:
            print response.message

    def do_quit(self, line):
        """quit

        exit from the command line.
        """
        return True

    def do_commit(self, line):
        """commit

        sends a commit to solr server
        """
        response = self.solr.commit()
        if response.satus == 200:
            print 'OK'
        else:
            print response.message
 
    def do_optimize(self, line):
        """commit

        sends optimize operation to solr server
        """
        response = self.solr.optimize()
        if response.satus == 200:
            print 'OK'
        else:
            print response.message

    def __highlight(self, data):
        formatted = json.dumps(data, indent=4)
        return highlight(formatted, formatter=TerminalFormatter(),
                         lexer=JavascriptLexer()).rstrip()


def main():
    SolrCLI().cmdloop()


if __name__ == '__main__':
    main()