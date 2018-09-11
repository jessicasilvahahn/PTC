#!/usr/bin/python3

import sys
import select
import fcntl
import os

op = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, op | os.O_NONBLOCK)

print('Digite alguma coisa ... você tem 5 segundos:')
r = select.select([sys.stdin],[],[], 5)

if r[0]:
  data = sys.stdin.read(1024)
  print('Você digitou:', data)
else:
  print('Timeout !')

sys.exit(0)
