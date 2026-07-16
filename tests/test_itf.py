import sys; sys.path.append(".") #lets python find the src folder
from src.ingest.itf import parse_line #imports the function under test

#the below are my text fixtures, inputs that I already know the corret outcome of
GOOD = "     /7239   4C2015 05 23.30928 11 55 25.17 -01 46 36.9          23.7 z1     T09"
SHORT = "0002I"

#the below runs the program on the "good" line.
rec = parse_line(GOOD)
assert rec is not None, "good line was rejected"

#the below ensures that the values we received from calling the parser function fit what they should be with the good line
assert rec["obscode"] == "T09", f"obscode wrong: {rec['obscode']}"
assert rec["desig"] == "/7239", f"desig wrong: {rec['desig']}"

assert parse_line(SHORT) is None, "short line was not rejected" #ensures that the short line was successfully rejected

print("all tests pass") #only passes if every assert "held", ensures the parser works

CONT = "0002IK19Q040  s2019 09 13.5327581 +   10.2502 + 5112.0801 + 4988.3508   ~01XrC53"
assert parse_line(CONT) is None, "continuation line was not rejected."