import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

wf = Workflow()
# Get query from Alfred
if len(wf.args):
  wf.save_password('inovex-inca-username', wf.args[0])
  print "INCA username got saved in Keychain"
else:
  wf.add_item('Please enter a username.',valid=False,icon=ICON_WARNING)
  print "Error"