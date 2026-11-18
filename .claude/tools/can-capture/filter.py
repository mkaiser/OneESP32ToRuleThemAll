import re
import sys

PREFIX = re.compile(r'\[[DVIW]\]\[Communication:\d+\]: ')
for line in sys.stdin:
    if 'Communication' in line:
        sys.stdout.write(PREFIX.sub(' ', line))
        sys.stdout.flush()
