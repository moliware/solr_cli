#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
solr_cli
~~~~~~~~

Command line client for solr. 

"""
import atexit
import json
import mysolr
import re
import readline
import signal
import sys

from blessings import Terminal
from os.path import expanduser
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JavascriptLexer, XmlLexer
from urlparse import parse_qs


__version__ = '0.2'


class SolrCLI(object):
    """ """

    require_connexion = (
        'ping', 'query', 'uri', 'commit', 'delete', 'optimize', 'schema',
        'fields'
    )

    def __init__(self, host=None, history_file=expanduser("~/.solr_cli")):
        self.solr = None
        self.connected = False
        self.term = Terminal()
        self.host = host
        self.history_file = history_file

        # Load history file
        try:
            readline.read_history_file(history_file)
        except IOError:
            pass
        atexit.register(self.__save_history)

        # Alias
        self.do_EOF = self.do_exit = self.do_quit

        # Registers tab for autocomplete
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind '\t' rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self.__completer)

        if host:
            self.do_connect(host)

        self.valid_commands = self.__get_commands()

    @property
    def prompt(self):
        connexion_name = self.host if self.host else 'disconnected'
        return '(%s)$ ' % connexion_name

    def __completer(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s 
                                for s in self.valid_commands
                                if s and s.startswith(text)]
            else:
                self.matches = self.valid_commands[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response

    def __get_commands(self):
        attributes = dir(self)
        commands = [attr[3:] for attr in attributes if attr.startswith('do_')]
        return sorted(commands)

    def __highlight(self, data):
        formatted = json.dumps(data, indent=4)
        return highlight(formatted, formatter=TerminalFormatter(),
                         lexer=JavascriptLexer()).rstrip()

    def __parse_line(self, line):
        index = line.find(' ')
        command = line
        tail = None
        if index > 0:
            command = line[:index]
            tail = line[index + 1:]
        return command, tail

    def __style_prompt(self):
        style = self.term.bold_green if self.connected else self.term.bold_red
        return style(self.prompt)

    def __save_history(self):
        readline.write_history_file(self.history_file)

    def loop(self):
        end = False
        while not end:
            try:
                line = raw_input(self.__style_prompt())
            except EOFError:
                line = 'EOF'
            line = line.strip()
            if not line:
                continue
            command, tail = self.__parse_line(line)
            if command in self.valid_commands:
                if self.connected or command not in self.require_connexion:
                    getattr(self, 'do_' + command)(tail)
                elif not self.connected and command in self.require_connexion:
                    print self.term.red('Connect to a solr server first')
            else:
                print self.term.red('Invalid command. Type help.')

    def help(self):
        pass

    def do_connect(self, host):
        """connect <solr_url>

        connects to a solr server located in solr_url. Example:

        connect http://localhost:8983/solr
        """
        if host:
            self.solr = mysolr.Solr(host)
            if self.solr.is_up():
                self.host = host
                self.connected = True
            else:
                print 'Cant\'t connect to %s' % host
        else:
            print self.do_connect.__doc__

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
        if query:
            response = self.solr.search(q=query)
            if response.status == 200:
                print self.__highlight(response.raw_content)
            else:
                print response.message
        else:
            print self.do_query.__doc__

    def do_uri(self, uri):
        """uri <params>

        makes a requests to a solr server allowing all paramaters. 
        'q' must be specified. Example:

        uri q=*:*&facet=true&facet.field=price&rows=0
        """
        params = parse_qs(uri)
        if 'q' in params:
            response = self.solr.search(**params)
            if response.status == 200:
                print self.__highlight(response.raw_content)
            else:
                print response.message
        else:
            print self.do_uri.__doc__

    def do_quit(self, line):
        """quit

        exit from the command line.
        """
        print 'Bye'
        exit(0)

    def do_commit(self, line):
        """commit

        sends a commit to solr server
        """
        response = self.solr.commit()
        if response.status == 200:
            print 'OK'
        else:
            print response.message

    def do_delete(self, query):
        """delete <q>

        Delete by query. Examples:

        Removes all the index::
            
            delete *:*
        
        Removes documents whose type is book ::

            delete type:"book"
        """
        if query:
            response = self.solr.delete_by_query(query)
            if response.status != 200:
                print response.message
        else:
            print self.do_query.__doc__
 
    def do_optimize(self, line):
        """commit

        sends optimize operation to solr server
        """
        response = self.solr.optimize()
        if response.status == 200:
            print 'OK'
        else:
            print response.message

    def do_schema(self, line):
        """schema

        prints the schema of the current index
        """
        schema = self.solr.schema()
        print highlight(schema, formatter=TerminalFormatter(),
                        lexer=XmlLexer()).rstrip()

    def do_fields(self, line):
        """fields

        prints the fields of the current schema
        """
        schema = self.solr.schema()
        search = re.search(r'<fields>.*?</fields>', schema, re.DOTALL)
        print highlight(search.group(0), formatter=TerminalFormatter(),
                        lexer=XmlLexer()).rstrip()


def main():
    host = sys.argv[1] if len(sys.argv) >= 2 else None
    SolrCLI(host).loop()


def bye(signal, frame):
    print 'Bye'
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, bye)
    main()