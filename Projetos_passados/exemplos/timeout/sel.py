#!/usr/bin/python3

import sys
import select
import fcntl
import os

op = fcntl.fcntl(0, fcntl.F_GETFL)
fcntl.fcntl(0, fcntl.F_SETFL, op | os.O_NONBLOCK)

print('Digite alguma coisa ... você tem 5 segundos:')
r = select.select([0],[],[], 5)

if r[0]:
  data = os.read(0, 1024)
  print('Você digitou:', data.decode('ascii'))
else:
  print('Timeout !')

sys.exit(0)
