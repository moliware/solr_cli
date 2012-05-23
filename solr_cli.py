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
        self.prompt = '(%s)$ ' % host
    
    def do_query(self, query):
        """query <q>

        makes a query to a solr server. Examples:

        query *:*
        query type:"book" AND price:[* TO 10]
        """
        try:
            response = self.solr.search(q=query)
            print self.__highlight(response.raw_response)
        except Exception, e:
            print e.message

    def do_uri(self, uri):
        """uri <uri>

        makes a requests to a solr server allowing all paramaters. Example:

        uri q=*:*&facet=true&facet.field=price&rows=0
        """
        try:
            response = self.solr.search(**parse_qs(uri))
            print self.__highlight(response.raw_response)
        except Exception, e:
            print e.message

    def do_quit(self, line):
        """quit

        exit from the command line.
        """
        return True

    def __highlight(self, data):
        formatted = json.dumps(data, indent=4)
        return highlight(formatted, formatter=TerminalFormatter(),
                         lexer=JavascriptLexer()).rstrip()


def main():
    SolrCLI().cmdloop()


if __name__ == '__main__':
    main()