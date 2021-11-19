# --------------------------------------------------------------------------------------------------
# This is an automated test script that will run `curl` shell commands and compare got results with
# expected responses. For this, we will write `curl` output to a temp file and read it from this
# Python script.
#* Important: this script is intended to run on Linux.
# --------------------------------------------------------------------------------------------------

from os import system # utility for executing OS shell commands
from sys import argv
import json
from typing import IO

# Using nice module for colored output, if available (you can install it through pip)
try:
    import colorama
    colorama.init(convert=False)
    def printOk(msg :str) -> None:
        print(colorama.Fore.LIGHTCYAN_EX, msg, colorama.Fore.RESET, sep="")
    def printError(msg :str) -> None:
        print(colorama.Fore.LIGHTRED_EX, msg, colorama.Fore.RESET, sep="")
except ImportError:
    def printOk(msg :str) -> None:
        print(msg)
    def printError(msg :str) -> None:
        print(msg)

TEMP_OUTPUT_FILE :str = "temp.json"

def printHelp() -> None:
    print(f"""Usage:
    {argv[0]} TGR_TARGET_HOST

Where TGR_TARGET_HOST is the LAN-level host IP of the machine in which the test are running. This is
needed for the PPE container in order to send the TGR confirmations properly, to be listened outside
the Docker environment (i.e. "localhost" won't work due the Docker networking).
""")

def main() -> int:
    if (len(argv) < 2 or argv[1] == "help"):
        printHelp()
        return 1
    
    LOCAL_LAN_IP :str = argv[1]

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
                "valid": true,
                "nombres": "LEANDRO ALBERTO",
                "apellido_paterno": "FERRERIA",
                "apellido_materno": "CIOBOTARU"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user?run=14343269-k" """,
            json.loads("""{
                "valid": false,
                "msg": "RUN inválido: no registrado"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user?run=empanada" """,
            json.loads("""{
                "valid": false,
                "msg": "RUN inválido: no registrado"
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4030/api/users/user" """,
            json.loads("""{
                "msg": "'run' query parameter is missing"
            }""") # status 400
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
                "valid": true
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
                "valid": false
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "run": "whatever",
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_paterno": "FERRERIA",
                    "apellido_materno": "CIOBOTARU"
                }'""",
            json.loads("""{
                "valid": false
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "CIoBOTARu"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: run, nombres, apellido_paterno, apellido_materno"
            }""") # status 400
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "run": "14343269-6",
                    "apellido_paterno": "ferreria",
                    "apellido_materno": "CIoBOTARu"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: run, nombres, apellido_paterno, apellido_materno"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "run": "14343269-6",
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_materno": "CIoBOTARu"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: run, nombres, apellido_paterno, apellido_materno"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4030/api/users/user" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "run": "14343269-6",
                    "nombres": "LEANDRO ALBERTO",
                    "apellido_paterno": "ferreria"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: run, nombres, apellido_paterno, apellido_materno"
            }""")
        ),

        ############################################################################################
        # RVM: licensePlateApplications
        #TODO: test format check for `numero_repertorio`.
        #TODO: test missing parameters check
        #TODO: test bad `tipo`
        #TODO: test bad `estado`
        #TODO: test bad `fecha` and `hora`
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
                ],
                "msg": "Con solicitudes pendientes",
                "success": false
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/licensePlates?patente=VRU-750" """,
            json.loads("""{
                "msg": "sin solicitudes pendientes",
                "success": true
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/licensePlates?patente=PatenteQueNoExiste" """,
            json.loads("""{
                "msg": "invalida",
                "success": false
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/licensePlates" """,
            json.loads("""{
                "msg": "Missing parameter: 'patente'"
            }""") # status 400
        ),

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
                "msg": "Uno o más IDs de dueño son inválidos para el vehiculo"
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
                "msg": "Uno o más IDs de dueño son inválidos para el vehiculo"
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
                "msg": "Placa inválida (no registrada)"
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
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/anotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: patente, tipo, numero_repertorio"
            }""") # status 400
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/anotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "tipo" : "PN",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: patente, tipo, numero_repertorio"
            }""") # status 400
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/anotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: patente, tipo, numero_repertorio"
            }""") # status 400
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
                    "aceptarORechazar": "rechazada",
                    "numero_repertorio" : "2021-45001"
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
                    "aceptarORechazar" : "rechazada",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "success": false,
                "msg": "No existe una anotación pendiente de ese tipo para ese vehículo"
            }""")
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/acceptRejectAnotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "tipo" : "PN",
                    "aceptarORechazar": "rechazada"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: patente, tipo, aceptarORechazar, numero_repertorio"
            }""") # status 400
        ),
        (
            """curl --location --request POST "http://localhost:4031/api/vehicles/acceptRejectAnotation" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "patente" : "BIF-933",
                    "numero_repertorio" : "2021-45001"
                }'""",
            json.loads("""{
                "msg": "One of the following parameters are missing: patente, tipo, aceptarORechazar, numero_repertorio"
            }""") # status 400
        ),

        ############################################################################################
        # RVM: develop_repertoryPlactesStatus
        ############################################################################################
        #TODO

        ############################################################################################
        # RVM: develop_getVehiclesOfPerson
        ############################################################################################
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/platesOfPerson?person_id=7900663-7" """,
            json.loads("""{
                "plates": [
                    "7900663-7",
                    "7900663-7"
                ]
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/platesOfPerson?person_id=foo" """,
            json.loads("""{
                "plates": []
            }""")
        ),
        (
            """ curl --location --request GET "http://localhost:4031/API/vehicles/platesOfPerson" """,
            json.loads("""{
                "msg": "Missing parameter: person_id"
            }""")
        ),

        ############################################################################################
        # PPE: ppePaymentRequest
        #* Note: in order to listen for the confirmation from outside of the Docker container, the
        #* `confirmation_ip` parameter must be your LAN level IP. See the README file.
        #TODO: test accidental double-payment detection
        ############################################################################################
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-22",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Pago Ingresado",
                "transaction_id": 2
            }""")
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-22",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Pago Ingresado",
                "transaction_id": 3
            }""")
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-22",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Pago Ingresado",
                "transaction_id": 4
            }""")
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "P0477420",
                    "numero_repertorio": "2007-10520",
                    "monto": 33.9,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP, # in this case, `id_persona` it is not a RUN, but a passport ID for the case of a non-chilean person.
            json.loads("""{
                "msg": "Pago Ingresado",
                "transaction_id": 5
            }""")
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "0477420",
                    "numero_repertorio": "2020-22",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Invalid parameter 'id_persona': must be a RUN/RUT (e.g. '12345678-k') or a passport number (e.g. 'P0123456')"
            }""") # status 400
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Invalid parameter 'numero_repertorio': bad format. Must match 'YEAR-number' with a maximum total lenght of 11 characters, and the YEAR must be in range [1800, 2021]"
            }""") # status 400
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Invalid parameter 'numero_repertorio': bad format. Must match 'YEAR-number' with a maximum total lenght of 11 characters, and the YEAR must be in range [1800, 2021]"
            }""") # status 400
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-5",
                    "numero_repertorio": "2020-84F",
                    "monto": 213540,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "Invalid parameter 'numero_repertorio': bad format. Must match 'YEAR-number' with a maximum total lenght of 11 characters, and the YEAR must be in range [1800, 2021]"
            }""") # status 400
        ),
        (
            """curl --location --request POST "localhost:4032/api/transaction/payment" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona": "1092093-K",
                    "numero_repertorio": "2007-10520",
                    "monto": -1,
                    "confirmation_ip": "%s"
                }'""" % LOCAL_LAN_IP,
            json.loads("""{
                "msg": "invalid paremeter 'monto': must be numberic and positive"
            }""") # status 400
        ),

        ############################################################################################
        # Caja: manualCreatePayment
        #TODO: test accidental double-payment detection
        #TODO: test format check for `numero_repertorio`
        #TODO: test missing params
        #TODO: test invalid `monto` (negative or non-numeric value)
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
            }""") #* `nuevo_folio` is the transaction/payment ID
        ),

        ############################################################################################
        # Caja: manualPaymentRefund
        ############################################################################################
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona" : "16248093-6",
                    "numero_repertorio" : "2018-404542",
                    "folio_ingreso": 51
                }'""",
            json.loads("""{
                "success": true,
                "msg": "Monto Reembolsado",
                "nuevo_folio": 1
            }""")
        ),
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona" : "16248093-6",
                    "numero_repertorio" : "2018-404542",
                    "folio_ingreso": 51
                }'""",
            json.loads("""{
                "success": false,
                "msg": "Reembolso denegado, no existen pagos en registro"
            }""")
        ),
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona" : "16248093-6",
                    "numero_repertorio" : "hello-world",
                    "folio_ingreso": 51
                }'""",
            json.loads("""{
                "success": false,
                "msg": "Reembolso denegado, no existen pagos en registro"
            }""")
        ),
        (
            """curl --location --request POST "localhost:4033/api/checkout/refund" \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "id_persona" : "pan",
                    "numero_repertorio" : "2018-404542",
                    "folio_ingreso": 51
                }'""",
            json.loads("""{
                "success": false,
                "msg": "Reembolso denegado, no existen pagos en registro"
            }""")
        )
    ]):
        if (len(argv) >= 2):
            command = command.replace("localhost", argv[1], 1)
        print("Running test #%d: %s" % (testNum, command))
        cmdExitCode :int = system("%s -sS -o %s" % (command, TEMP_OUTPUT_FILE)) # adding flags for silent curl, show errors and output to the desired file instead of `stdout`
        if (cmdExitCode != 0):
            print("Test #%d failed: curl command returned with error code %d" % (testNum, cmdExitCode))
            return 2
        tempFile :IO = open(file=TEMP_OUTPUT_FILE, mode="rt", encoding="utf-8") # we will read contents written by `curl` command in that file for each test from Python (yes, we have to open it on each test)
        gotResult :dict = json.loads(tempFile.read())
        tempFile.close()
        if (expectedResult != gotResult):
            printError("Test #%d failed" % testNum)
            print("Expected %s, but got %s" % (expectedResult, gotResult))
            return 3

    system("rm -f %s" % TEMP_OUTPUT_FILE) # removing temporal file
    print()
    printOk("Yay! All tests passed")
    return 0

if (__name__ == "__main__"):
    exit(main())
