from patterns import *
import re

s = "Привет, сколько времени?"
if re.match(pattern_hello, s.lower()) is not None:
    print("Hello")
if re.match(pattern_time, s.lower()) is not None:
    print("time")