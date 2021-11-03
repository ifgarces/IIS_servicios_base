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
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
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
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
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
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
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
        # RVM: licensePlateApplications
        ############################################################################################
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/licensePlates?patente=BIF-933" """,
            json.loads("""{
                "solicitudes": [
                    {
                        "numero_repertorio": "2016-437",    
                        "fecha": "1986-07-13T00:00:00.000Z",
                        "hora": "03:23:30",
                        "tipo": "AlzPN",
                        "estado": "ingresada"
                    }
                ]
            }""")
        ), #TODO: add fail test scenario

        ############################################################################################
        # RVM: licensePlateCheck
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4031/API/vehicles/licensePlates" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933"
                }'""",
            json.loads("""{
                "valid": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/API/vehicles/licensePlates" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente": "queso"
                }'""",
            json.loads("""{
                "valid": false
            }""")
        ),

        ############################################################################################
        # RVM: ownershipCheck
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "plate": "BIF-933",
                    "owners": [
                        "4342908-6",
                        "13413217-5",
                        "6559196-0",
                        "11257169-8",
                        "9308502-7"
                    ]
                }'""",
            json.loads("""{
                "valid": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "plate": "BIF-933",
                    "owners": [
                        "4342908-6",
                        "13413217-5",
                        "something"
                    ]
                }'""",
            json.loads("""{
                "valid": false,
                "msg": "Invalid owners"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "plate": "bif-933",
                    "owners": [
                        "11257169-8"
                    ]
                }'""",
            json.loads("""{
                "valid": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "plate": "BIF-933",
                    "owners": [
                        "4342908-6",
                        "13413217-5",
                        "6559196-0",
                        "11257169-8",
                        "9308502-7",
                        "1231231-2"
                    ]
                }'""",
            json.loads("""{
                "valid": false,
                "msg": "Invalid owners"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/check_ownership" \
                --header 'Content-Type: application/json' \
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

        ############################################################################################
        # RVM: addAnnotations
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/anotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "msg": "Anotacion creada"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/anotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "msg": "Ya hay una anotacion de ese tipo para ese vehiculo, por favor apruebela o rechasela antes de ingresar otra"
            }""")
        ),

        ############################################################################################
        # RVM: acceptOrRejectAnnotation
        ############################################################################################
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/acceptRejectAnotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN",
                    "aceptarORechazar" : "rechazada"
                }'""",
            json.loads("""{
                "success": true
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/acceptRejectAnotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN",
                    "aceptarORechazar" : "rechazada"
                }'""",
            json.loads("""{
                "success": false,
                "msg": "No existe una anotación pendiente de ese tipo para ese vehículo"
            }""")
        ),

        ############################################################################################
        # Caja: manualCreatePayment
        ############################################################################################
        (
            """curl --location --request POST "localhost:4033/api/checkout/pay" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "numero_repertorio" : "2018-404542",
                    "id_persona" : "16248093-6",
                    "monto" : 22.5
                }'""",
            json.loads("""{
                "success": true,
                "msg": "Monto Ingresado",
                "nuevo_folio": 51
            }""")
        ), #TODO: test the fail scenario for this call

        ############################################################################################
        # Caja: manualPaymentRefund
        ############################################################################################
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "folio": 51,
                    "id_persona" : "16248093-6",
                    "numero_repertorio" : "2018-404542"
                }'""",
            json.loads("""{
                "success": true,
                "msg": "Monto Reembolsado",
                "nuevo_folio": 52
            }""")
        ),
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "folio": 51,
                    "id_persona" : "16248093-6",
                    "numero_repertorio" : "2018-404542"
                }'""",
            json.loads("""{
                "msg": "Reembolso denegado"
            }""") #TODO: [FIX] I would like a `"success": false` parameter in the response...
        ),

        ############################################################################################
        # PPE: ppePaymentRequest
        ############################################################################################
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-22",
                    "monto": 213540
                }'""",
            json.loads("""{
                "msg": "Pago Ingresado",
                "t_id": 2
            }""")
        )
    ]):
        print("Running test #%d: %s" % (testNum, command))
        cmdExitCode :int = system("%s -sS -o %s" % (command, TEMP_OUTPUT_FILE)) # adding flags for silent curl, show errors and output to the desired file instead of `stdout`
        if (cmdExitCode != 0):
            print("Test #%d failed: the following command returned with error code %d:" % (testNum, cmdExitCode))
            print(command)
            return 1
        tempFile :IO = open(file=TEMP_OUTPUT_FILE, mode="rt", encoding="utf-8") # we will read contents written by `curl` command in that file for each test from Python (yes, we have to open it on each test)
        gotResult :dict = json.loads(tempFile.read())
        tempFile.close()
        if (expectedResult != gotResult):
            logError("Test #%d failed" % testNum)
            print("Expected %s, but got %s" % (expectedResult, gotResult))
            return 2

    system("rm %s" % TEMP_OUTPUT_FILE) # removing temporal file
    print()
    logOk("Yay! All tests passed")
    return 0

if (__name__ == "__main__"):
    exit(main())
