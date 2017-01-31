import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

wf = Workflow()

if len(wf.args):
  wf.save_password('inovex-inca-password', wf.args[0])
  print "INCA password got saved in Keychain"
else:
  wf.add_item('Please enter a password.',valid=False,icon=ICON_WARNING)
  print "Error"