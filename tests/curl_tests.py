# --------------------------------------------------------------------------------------------------
# This is an automated test script that will run `curl` shell commands and compare got results with
# expected responses. For this, we will write `curl` output to a temp file and read it from this
# Python script.
#* Important: this script is intended to run on Linux.
# --------------------------------------------------------------------------------------------------

from os import system
from time import sleep
import json
from typing import IO

# SERVER_IP :str = "localhost"
TEMP_OUTPUT_FILE :str = "temp.json"

def main() -> int:
    system("touch %s" % TEMP_OUTPUT_FILE) # creating temp file if needed

    # Here we itarate over a list of tuples with the curl command and the expected parsed JSON with
    # the `json.loads` utility
    for testNum, (command, expectedOut) in enumerate([
        # --- SRCEI ---
        (
            f"curl --location --request GET 'localhost:4030/api/users/user?run=14343269-6'",
            json.loads("""{
                "userFirstName": "LEANDRO ALBERTO",
                "userLastName": "FERRERIA",
                "userRun": "14343269-6"
            }""")
        ),
        (
            """curl --location --request POST 'localhost:4030/api/users/user' \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "run": "14343269-6",
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "CIoBOTARu",
                    "fecha_nacimiento": "1992-08-07"
                }'""",
            json.loads("""{
                "msg": "Usuario existente"
            }""")
        )
    ]):
        print("Running test #%d..." % testNum)
        exitCode = system(command + " -sS -o %s" % TEMP_OUTPUT_FILE) # adding flags for silent curl, show errors and output to the desired file instead of `stdout`
        if (exitCode != 0):
            print("Test #%d failed: command \"%s\" returned with error code %d" % (testNum, command, exitCode))
            return 1
        tempFile = open(file=TEMP_OUTPUT_FILE, mode="rt", encoding="utf-8") # we will read contents written by `curl` command in that file for each test from Python (yes, we have to open it on each test)
        rawOutput = tempFile.read()
        print(rawOutput)
        gotOutput = json.loads(rawOutput)
        tempFile.close()
        if (expectedOut != gotOutput):
            print("Test #%d failed: expected %s, but got %s" % (testNum, expectedOut, gotOutput))
            return 2

    print()
    print("ALL TESTS PASSED")
    return 0

if (__name__ == "__main__"):
    exit(main())
