import secretary
import subprocess
from datetime import datetime
import sys



if sys.argv[1] == 'make':
	process = subprocess.Popen(['open',datetime.now().strftime('%Y.%m.%d') + '.docx'])

#if sys.argv[1] is 'to-pdf':