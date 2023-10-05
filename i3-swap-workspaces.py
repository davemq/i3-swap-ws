#!/usr/bin/env python3

from i3ipc import Connection
from itertools import cycle
import logging
import time

#logging.basicConfig(level=logging.DEBUG)

# Open i3 connection
i3 = Connection()

# - Get list of outputs
# - remove inactive
outputs = [o for o in i3.get_outputs() if o.active]

# - sort by rect.x
outputs.sort(key = lambda o: o.rect.x)

# - create a cycle iterator from the list
co = cycle(outputs)

# - Get workspaces
workspaces = i3.get_workspaces()
# - Find focused
w = [w for w in workspaces if w.focused]
w = w[0]
name = w.name
output = w.output
logging.debug(f'w {w} name {name} output {output}')

# Figure out "next" output and its workspace.
n = None                        # covers not finding a match!
for c in co:
    if c.name == output:
        n = next(co)
        next_workspace = n.current_workspace
        next_name = n.name
        logging.debug(f'next_workspace {next_workspace} next_name {next_name}')
        break
        
# Handle case where there's only 1 output, i.e. do nothing!
if n == output:
    logging.debug(f'n {n} == output {output}, exiting')
    exit(0)

# Move focused workspace to next
logging.debug(f'move workspace to output {next_name}')
cr = i3.command(f'move workspace to output {next_name}')
if not cr[0].success:
    raise RuntimeError(cr[0].error)
time.sleep(0.1)
cr = logging.debug(f'workspace {next_workspace}')
cr = i3.command(f'workspace {next_workspace}')
if not cr[0].success:
    raise RuntimeError(cr[0].error)
time.sleep(0.1)
cr = logging.debug(f'move workspace to output {output}')
cr = i3.command(f'move workspace to output {output}')
if not cr[0].success:
    raise RuntimeError(cr[0].error)
time.sleep(0.1)
cr = logging.debug(f'workspace {name}')
cr = i3.command(f'workspace {name}')
if not cr[0].success:
    raise RuntimeError(cr[0].error)

exit(0)
