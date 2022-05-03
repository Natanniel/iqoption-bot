#!/usr/bin/python
from subprocess import Popen

p = Popen("python main.py", shell=True)
p.wait()