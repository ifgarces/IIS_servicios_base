# --------------------------------------------------------------------------------------------------
# This is an automated test script that will run `curl` shell commands and compare got results with
# expected responses. For this, we will write `curl` output to a temp file and read it from this
# Python script.
#* Important: this script is intended to run on Linux.
# --------------------------------------------------------------------------------------------------

from os import system # utility for executing OS shell commands
import json
from typing import IO

# Using nice module for colored output, if available (you can install it through pip)
try:
    import colorama
    colorama.init(convert=False)
    def logOk(msg :str) -> None:
        print(colorama.Fore.LIGHTCYAN_EX, msg, colorama.Fore.RESET, sep="")
    def logError(msg :str) -> None:
        print(colorama.Fore.LIGHTRED_EX, msg, colorama.Fore.RESET, sep="")
except ImportError:
    def logOk(msg :str) -> None:
        print(msg)
    def logError(msg :str) -> None:
        print(msg)

TEMP_OUTPUT_FILE :str = "temp.json"

def main() -> int:
    system("touch %s" % TEMP_OUTPUT_FILE) # creating temp file if needed

    # Here we itarate over a list of tuples with the curl command and the expected parsed JSON with
    # the `json.loads` utility
    for testNum, (command, expectedResult) in enumerate([
        ############################################################################################
        # SRCEI: simpleCheck
        ############################################################################################
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user?run=14343269-6" """,
            json.loads("""{
                "nombres": "LEANDRO ALBERTO",
                "apellido_paterno": "FERRERIA",
                "apellido_materno": "CIOBOTARU"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user?run=14343269-k" """,
            json.loads("""{
                "msg": "RUN inválido: no registrado"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user?run=empanada" """,
            json.loads("""{
                "msg": "RUN inválido: no registrado"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user" """,
            json.loads("""{
                "msg": "Must provide run parameter"
            }""")
        ),

        ############################################################################################
        # SRCEI: strictCheck
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "run": "14343269-6",
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "CIoBOTARu"
                }'""",
            json.loads("""{
                "msg": "Usuario existente"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "run": "14343269-6",
                    "nombres": "Hello",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "CIoBOTARu"
                }'""",
            json.loads("""{
                "msg": "Usuario no existe"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "run": "whatever",
                    "nombres": "leandro alberto",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "ciobotaru"
                }'""",
            json.loads("""{
                "msg": "Usuario no existe"
            }""")
        ),

        ############################################################################################
        # Caja: manualCreatePayment
        ############################################################################################
        # (
        #     """curl --location --request POST "http://localhost:4033/api/checkout/pay" \\
        #         --header 'Content-Type: application/json' \\
        #         --data-raw '{
        #             "RUN": "16248093-6",
        #             "monto": "22700"
        #         }'""",
        #     json.loads("""{
        #         "msg": "Monto Ingresado"
        #     }""")
        # ),

        # ############################################################################################
        # # Caja: manualPaymentRefund
        # ############################################################################################
        # (
        #     """curl --location --request POST "http://localhost:4033/api/checkout/refund" \\
        #         --header 'Content-Type: application/json' \\
        #         --data-raw '{
        #             "RUN": "16248093-6",
        #             "monto": "21821.74"
        #         }'""",
        #     json.loads("""{
        #         "msg": "Monto Retirado"
        #     }""")
        # ),

        ############################################################################################
        # RVM: ownershipCheck
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "plate": "LEC-681",
                    "owners": [
                        "4930477-3",
                        "10651736-3",
                        "14652074-K"
                    ]
                }'""",
            json.loads("""{
                "valid": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "plate": "LEC-681",
                    "owners": [
                        "4930477-3",
                        "10651736-3",
                        "something"
                    ]
                }'""",
            json.loads("""{
                "valid": false,
                "msg": "Invalid owners"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "plate": "lec-681",
                    "owners": [
                        "14652074-k"
                    ]
                }'""",
            json.loads("""{
                "valid": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "plate": "LEC-681",
                    "owners": [
                        "4930477-3",
                        "10651736-3",
                        "14652074-0"
                    ]
                }'""",
            json.loads("""{
                "valid": false,
                "msg": "Invalid owners"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \\
                --header 'Content-Type: application/json' \\
                --data-raw '{
                    "plate": "sopaipilla",
                    "owners": [
                        "4930477-3"
                    ]
                }'""",
            json.loads("""{
                "valid": false,
                "msg": "Invalid plate"
            }""")
        ),
    ]):
        print("Running test #%d..." % testNum)
        cmdExitCode :int = system("%s -sS -o %s" % (command, TEMP_OUTPUT_FILE)) # adding flags for silent curl, show errors and output to the desired file instead of `stdout`
        if (cmdExitCode != 0):
            print("Test #%d failed: command \"%s\" returned with error code %d" % (testNum, command, cmdExitCode))
            return 1
        tempFile :IO = open(file=TEMP_OUTPUT_FILE, mode="rt", encoding="utf-8") # we will read contents written by `curl` command in that file for each test from Python (yes, we have to open it on each test)
        gotResult :dict = json.loads(tempFile.read())
        tempFile.close()
        if (expectedResult != gotResult):
            logError("Test #%d failed: expected %s, but got %s" % (testNum, expectedResult, gotResult))
            logError("The curl command for the failed test is %s" % command)
            return 2

    system("rm %s" % TEMP_OUTPUT_FILE) # removing temporal file
    print()
    logOk("Yay! All tests passed")
    return 0

if (__name__ == "__main__"):
    exit(main())
