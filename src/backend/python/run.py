#!/usr/bin/python2.7

"""
	An entry point to run the backend.
"""

import sys, getopt

from Main import Main

def main(argv):
   interface = None
   output = None
   clean = False

   help_message = 'run.py -i <interface> --clean-existing -o <output>'

   try:
      opts, args = getopt.getopt(argv,'hi:o:c', ['clean-existing'])

   except getopt.GetoptError as error:
      print error
      sys.exit(2)

   print opts, args

   for opt, arg in opts:
      if opt == '-h':
         print help_message

      elif opt in ('-i'):
         if str(arg) == "list":
            'TODO print interfaces'
         else:
            interface = arg

      elif opt in ('-o'):
         output = arg

      elif opt in ('-c', '--clean-existing'):
         clean = True

   if (output or interface) == None:
      print help_message
      sys.exit()

   Main(interface, output, clean)

if __name__ == '__main__':
   main(sys.argv[1:])