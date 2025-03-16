import os
import re
import sys


assert len(sys.argv) > 1
input_path = sys.argv[1]

with open(input_path, "r") as fin:
    output = fin.read()
    while True:
        match = re.search(r"\$\{([^\}]+)\}", output)
        if match is None:
            break
        value = os.getenv(match.group(1))
        assert value is not None, f"Missing env variable {match.group(1)}"
        output = output.replace(match.group(0), value)
    print(output, end="")
