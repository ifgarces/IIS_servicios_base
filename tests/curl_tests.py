# --------------------------------------------------------------------------------------------------
# This is an automated test script that will run `curl` shell commands and compare got results with
# expected responses. For this, we will write `curl` output to a temp file and read it from this
# Python script.
# --------------------------------------------------------------------------------------------------

from os import system
import json
from typing import IO

SERVER_IP :str = "localhost"
TEMP_OUTPUT_FILE :str = "temp.json"

def main() -> int:
    system("touch %s" % TEMP_OUTPUT_FILE) # creating temp file if needed

    # We will read contents written by `curl` command in that file for each test from Python

    tempFile :IO = open(file=TEMP_OUTPUT_FILE, mode="rt", encoding="utf-8")
    exitCode :int

    for index, (command, expectedOut) in enumerate([
        (
            f"curl --location --request GET '{SERVER_IP}:4030/api/users/user?run=14343269-6'",
            json.loads("""{
                "userFirstName": "LEANDRO ALBERTO",
                "userLastName": "FERRERIA",
                "userRun": "14343269-6"
            }""")
        )
    ]):
        exitCode = system(command + " -o %s" % TEMP_OUTPUT_FILE)
        if (exitCode != 0):
            print("Error: command \"%s\" returned with error code %d" % (command, exitCode))
            tempFile.close()
            return 1
        gotOutput = json.loads(tempFile.read())
        if (expectedOut != gotOutput):
            print("Error: unexpected result for test #%d. Expected %s, but got %s" % (index, expectedOut, gotOutput))
            tempFile.close()
            return 2

    tempFile.close()
    print()
    print("ALL TESTS PASSED")
    return 0

if (__name__ == "__main__"):
    exit(main())
