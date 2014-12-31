#!/usr/bin/python
#
# wrapper script for pylint which just shows the errors and changes the return value if there's problems
# (enforcing a minscore and/or maxerrors - defaults to perfection)
#
import sys, re, subprocess, os

MINSCORE = 10.0
MAXERRORS = 0
    
command = 'pylint --rcfile=pylintrc --disable=W0511,W9911,W9913 `find webui python_saml libs -name "*py"`'

# unbuffer *both* me and the pylint subprocess!
os.environ['PYTHONUNBUFFERED'] = '1'
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     shell=True, universal_newlines=True)
num_errors = 0
score = 0
while True:
    line = p.stdout.readline().strip()
    if line is None:
        break
    match = re.search(r'^.+?:[0-9]+: \[.[0-9]+.+?\] ', line)
    if match:
        print line
        num_errors += 1
        continue
    match = re.search(r'Your code has been rated at ([0-9.-]+)', line)
    if match:
        score = float(match.group(1))
        break

if score < MINSCORE:
    print "scored %.2f which is less than %.2f - aborting" % (score, MINSCORE)
    sys.exit(3)
if num_errors < MAXERRORS:
    print "%d errors which is more than %d - aborting" % (num_errors, MAXERRORS)
    sys.exit(4)
