"""
Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying.
"""

import re
import sys
from json import dumps
from we_get.core.utils import printc
from we_get.core.utils import printc_raw
from we_get.core.utils import color
from we_get.core.utils import msg_item
from we_get.core.utils import msg_error
from we_get.core.commands import COMMANDS
from we_get.core.completer import WGCompleter
from we_get.core.style import we_get_prompt_style
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

class shell(object):
    def __init__(self):
        self.prompt = None
        self.pargs = None
        self.items = None
        self.show_links = False

    def prompt_usage(self):
        printc("white", "Usage: help")
        printc("yellow", "\nOptions:")
        for x in COMMANDS:
            print("  {0}  {1}".format(color("blue", x), 
                color("white", COMMANDS[x]['help'])))

    def prompt_is_single_command(self, command):
        if len(command.split()) == 1:
            return True
        return False

    def prompt_no_command(self, command):
        if not command:
            return True
        return False

    def prompt_show_items(self):
        for item in self.items:
            msg_item(item, self.items[item])

    def prompt_verify_command(self, command, args):
        for x in COMMANDS:
            if x == command and COMMANDS[x]['required_argument'] and not args:
                printc("white", 'Usage: {0} {1} ...'.format(x, COMMANDS[x]['usage']))
                printc("yellow", "\nOptions:");
                for opt in COMMANDS[x]['opts']:
                    printc_raw("blue", "  %s" %(opt))
                    printc("white", "\t%s" % (COMMANDS[x]['opts'][opt]))
                return False
        return True

    def prompt_command_show(self, args):
        _ = args.split()
        torrent = _[0]
        _.pop(0)
        if _:
            args = _[0]
        else:
            args = None
    
        """In this method we can use regex in the torrent name.
           for example only show torrents with 'S0\d' string.
            
           more exmaples:
            show .Cool --link # Show all torrents with .Cool
            show Cool.Torrent\d --target
        """
        if torrent in self.items.keys():
            items_idx = [torrent]
        else:
            try:
                items_idx = [item for i, item in enumerate(self.items.keys()) if re.search(torrent, item)]
            except Exception as e:
                msg_error("Invalid regular expression or torrent name.", False)
                return

        for x in items_idx:
            if args == '--link':
                print(self.items[x]['link'])
            elif args == "--target":
                print("%s src(%s)" % (color("cyan", x), color("yellow", self.items[x]['target'])))
            elif args == "--seeds":  
                print("%s se(%s)" % (color("cyan", x), color("green", self.items[x]['seeds'])))
            elif args == "--leeches":
                print("%s le(%s)" % (color("cyan", x), color("red", self.items[x]['leeches'])))
            else:
                print("%s %s" %(x, dumps(self.items[x], indent=2, sort_keys=True)))

    def prompt_parse_command(self, command, args):
        if command == "show":
            self.prompt_command_show(args)
        elif command in ('list', 'l'):
            self.prompt_show_items()
        elif command in ('help', 'h', '?'):
            self.prompt_usage()
        elif command in ('exit', 'q', 'quit'):
            return False
        else:
            if not command.split()[0] in COMMANDS:
                msg_error("No such command.", False)
        return True
        
        
    def shell(self, items, pargs):
        """ select_shell: run a select shell on the items.
            @param items: self.items dict().
            @param pargs: provided arguments dict().
        """
        self.pargs = pargs
        self.items = items
        history = InMemoryHistory()
        sys.stdout.write('\n') # when msg_fetching ends.
        self.prompt_show_items()

        while True:
            p = prompt(u'we-get > ', history=history,
            auto_suggest=AutoSuggestFromHistory(),
            completer=WGCompleter(list(self.items.keys())), 
            style=we_get_prompt_style)

            if self.prompt_no_command(p):
                continue
            elif self.prompt_is_single_command(p):
                command = p
                args = None
            else:
                _ = p.split()
                command = _[0]
                _.pop(0)
                args = ' '.join(_)
            if not self.prompt_verify_command(command, args):
                continue
            elif not self.prompt_parse_command(command, args):
                break
