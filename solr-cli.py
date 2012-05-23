# -*- coding: utf-8 -*-
"""
solr-cli
~~~~~~~~



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
        self.solr = mysolr.Solr(host)
        self.prompt = '(%s)$ ' % host
    
    def do_query(self, query):
        try:
            response = self.solr.search(q=query)
            print self.__highlight(response.raw_response)
        except Exception, e:
            print e.message

    def do_uri(self, uri):
        try:
            response = self.solr.search(**parse_qs(uri))
            print self.__highlight(response.raw_response)
        except Exception, e:
            print e.message

    def do_EOF(self, line):
        return True

    def do_quit(self, line):
        return True

    def __highlight(self, data):
        formatted = json.dumps(data, indent=4)
        return highlight(formatted, formatter=TerminalFormatter(),
                         lexer=JavascriptLexer()).rstrip()

if __name__ == '__main__':
    SolrCLI().cmdloop()
