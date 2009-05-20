# -*- coding: utf-8 -*-

import logging
import os
import sys

import kay
kay.setup()

from kay.app import get_application
from kay.utils.handlers import KayHandler
from kay.conf import settings

_debugged_application = None

def real_main():
  application = get_application()
  if settings.DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      # use our debug.utils with Jinja2 templates
      import debug.utils
      sys.modules['werkzeug.debug.utils'] = debug.utils

      # don't use inspect.getsourcefile because the imp module is empty 
      import inspect
      inspect.getsourcefile = inspect.getfile
    
      # wrap the application
      from werkzeug import DebuggedApplication
      global _debugged_application
      if _debugged_application is None:
        _debugged_application = application = DebuggedApplication(application,
                                                                  evalex=True)
      else:
        application = _debugged_application
  else:
    logging.getLogger().setLevel(logging.INFO)
  KayHandler().run(application)

def profile_main():
  # This is the main function for profiling 
  # We've renamed our original main() above to real_main()
  import cProfile, pstats
  prof = cProfile.Profile()
  prof = prof.runctx("real_main()", globals(), locals())
  print "<pre>"
  stats = pstats.Stats(prof)
  stats.sort_stats("time")  # Or cumulative
  stats.print_stats(80)  # 80 = how many to print
  # The rest is optional.
  # stats.print_callees()
  # stats.print_callers()
  print "</pre>"

if settings.PROFILE:
  main = profile_main
else:
  main = real_main

if __name__ == '__main__':
  main()