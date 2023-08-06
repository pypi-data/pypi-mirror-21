"""
Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying.
"""

import collections
import re
from collections import OrderedDict
from sys import exit
from json import dumps
from docopt import docopt
from importlib import import_module
from we_get.core.utils import format_help
from we_get.core.utils import msg_error
from we_get.core.utils import msg_info
from we_get.core.utils import msg_err_trace
from we_get.core.utils import msg_warning
from we_get.core.utils import msg_fetching
from we_get.core.utils import list_wg_modules

__version__ = "1.0"
__doc__ = """Usage: we-get [options]...

Options:
  -s --search=<text>    Search for a torrent.
  -l --list             List top torrents from modules.
  -t --target=<target>  Select module to use or \'all\'.
  -L --links            Output results as links.
  -J --json             Output results in JSON format.
  -G --get-list         List targets (supported web-sites).
  -f --filter=<str>     Match text or regular expression in the torrent name.
  -n --results=<n>      Number of results to retrieve.
  -S --sort-type=<type> Sort torrents by name/seeds (default: seeds).

Video options:
  -q --quality=<q>      Try to match quality for the torrent (720p,1080p, ...).
  -g --genre=<g>        Try to select video genre for the torrent (action, comedy, etc..).

General options:
  -h --help             Help message.
  -v --version          Show version.
"""

class wg_select(object):
    """ Select which modules to run """
    def __init__(self, pargs):
        self.pargs = pargs
        self.modules = list()
        self.targets = list()
        self.items = dict()
        self.results_type = None
        self.results = None
        self.filter = None
        self.parse_args()
        self.sort_type = None

    def parse_args(self):
        for arg in self.pargs:
            if arg == "--filter" or arg == "--quality":
                self.filter = self.pargs[arg][0]
            elif arg == "--results":
                self.results = int(self.pargs[arg][0])
            elif arg == "--target":
                self.targets = self.pargs[arg][0].split(',')
            elif arg == '--links':
                self.results_type = 'L'
            elif arg == '--json':
                self.results_type = 'J'
            elif arg == "--sort":
                self.sort_type = self.pargs[arg][0]

    def cut_items(self, items, results):
        """cut_items: show N items. 
        """	
        nitems = dict()
        for key in sorted(items)[:results]:
            nitems.update({ key : items[key]})
        return nitems

    def filter_items(self, fx):
        """filter_items: match text or regex in the torrent name.
        """
        nitems = dict()
        for item in self.items:	
            if re.findall(fx, item):
                nitems.update({item : self.items[item] })	
        return nitems


    def add_items_label(self, target, items):
        """ add_items_label - add label of the target to the torrent name.
            @param target
            @param items
        """
        nitems = dict()

        for item in items:
            items[item].update({"target" : target })
            nitems.update({ item : items[item] })
        return nitems

    def sort_items_by_seeds(self, items):
        nitems = OrderedDict()

        # Sort by number of seeds
        i = sorted(items, key = lambda x: int(items[x]['seeds']), reverse=True)
        for item in i:
            nitems.update({ item : items[item] })
        return nitems

    def sort_items_by_name(self, items):
        return collections.OrderedDict(sorted(items.items())) 

    def run(self):
        items = dict()

        if self.targets[0] == "all":
            self.targets.pop()
            self.targets = list_wg_modules()

        for target in self.targets:
            if not self.results_type:
                msg_fetching(target)
            path = "we_get.modules.%s" %(target)
            try:
                run = import_module(path)	
            except ImportError:
                msg_error("Cannot find target \'%s\'." % (target), True)
            except Exception:
                msg_info("Module: \'%s.py\' stopped!" % (target));
                msg_err_trace(True)
            items = run.main(self.pargs)
            items = self.add_items_label(target, items)
            if items: 
                self.items.update(items)
            else:
                msg_error(" \'%s\' - no results" % (target), False)
   
        if not self.items:
            return
        if self.filter:  
            self.items = self.filter_items(self.filter)
        if self.results:
            self.items = self.cut_items(self.items, self.results)
        if self.sort_type == "name":
            self.items = self.sort_items_by_name(self.items)
        else:
            self.items = self.sort_items_by_seeds(self.items)
        
        if self.results_type == 'J':
            print(dumps(self.items, indent=2, sort_keys=True))
        elif self.results_type == 'L':
            [print(self.items[item]['link']) for item in self.items]
        else:
            # XXX: import we_get.core.shell is here for optimization.
            # we-get will load 50% faster!
            from we_get.core.shell import shell
            self.shell = shell()
            self.shell.shell(self.items, self.pargs)
    
class WG(object):
    """ Main module """
    def __init__(self):
        self.arguments = None
        self.parguments = dict()
        self.we_get_run = 0 ## This variable check if the provided arguments has been provided.

    def get_provided_arguments(self):
        """ provoded_arguments:
            return all of the arguments with a value.
        """
        parg = dict()
        for arg in self.arguments:
            if self.arguments[arg]: parg.update({arg : self.arguments[arg]})
        return parg

    def parse_arguments(self):
        self.arguments = docopt(__doc__, help=False)
        self.parguments = self.get_provided_arguments()

        if not self.parguments or '--help' in self.parguments:
            format_help(__doc__, None)
            exit(0)
        elif '--version' in self.parguments:
            print(__version__)
            exit(0)
        elif '--get-list' in self.parguments:
            [print(module) for module in list_wg_modules()]
            exit(0)
        elif '--list' in self.parguments or '--search' in self.parguments:
            if '--target' in self.parguments:
                self.we_get_run = 1
        if self.we_get_run != 1:
            format_help(__doc__, "Use --search/--list with --target.")
            exit(1)

    def start(self):
        sel = wg_select(self.parguments)
        sel.run()
