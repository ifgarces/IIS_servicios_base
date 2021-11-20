# RVM API

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

Every annotation has a type and a status, which possible values are stated in the tables 1 and 2, respectively.

License plate format: it is composed of three uppercase letters, a hyphen and three numbers as can be seen in the following example (e.g. `"BIF-933"`).

For any call, if there are missing parameters (e.g. in the request query or body), the server will return a response with status 400 BAD REQUEST and a body with a `msg` explaining the reason of the invalid request. When a request triggers an exception in the server, its response will have status 500 and will have this body: `{msg: 'Internal Server Error'}`.

The repertoire ID has the format "YEAR-NUMBER", e.g. "2014-283".

Note: in the RVM, the owner(s) can be any kind of person: natural or not (enterprise) and chilean or not (for foreigners, the ID is a passport number, not a RUN). Approximately, 25% of the persons are enterprises (non-natural) and, from the natural ones, 10% are foreigners. The passport ID is a string starting with a "P" character, followed by numbers, e.g. "P01616026". The format for the RUT is exactly the same than the RUN, but it is possible to check if a national person is natural or not by querying the SRCEI (if it is not a valid RUN, then it is a RUT).

| Annotation type | Description                  |
| --------------- | ---------------------------- |
| `"PN"`          | *Prenda*.                    |
| `"PH"`          | *Prohibición*.               |
| `"AlzPN"`       | *Alzamiento de prenda*.      |
| `"AlzPH"`       | *Alzamiento de prohibición*. |
| `"CA"`          | *Cambio de acreedor*.        |

Table 1: annotation types.

| Annotation status | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| `"ingresada"`     | Entered, but pending validation status (accept or reject this annotation). |
| `"aceptada"`      | Annotation accepted.                                                       |
| `"rechazada"`     | Annotation rejected.                                                       |

Table 2: annotation statuses.

- [RVM API](#rvm-api)
  - [1. GET: Check Vehicle Anotations](#1-get-check-vehicle-anotations)
    - [1.1. Request query format](#11-request-query-format)
    - [1.2. Example calls](#12-example-calls)
    - [1.3. Expected responses](#13-expected-responses)
  - [2. POST: Check if a vehicle exist in the RVM DB](#2-post-check-if-a-vehicle-exist-in-the-rvm-db)
    - [2.1. Request body format](#21-request-body-format)
    - [2.2. Example calls](#22-example-calls)
    - [2.3. Expected responses](#23-expected-responses)
  - [3. POST: check ownership of a plate](#3-post-check-ownership-of-a-plate)
    - [3.1. Request body format](#31-request-body-format)
    - [3.2. Example calls](#32-example-calls)
  - [4. POST: create new annotation for a plate](#4-post-create-new-annotation-for-a-plate)
    - [4.1. Request body format](#41-request-body-format)
    - [4.2. Example calls](#42-example-calls)
    - [4.3. Expected responses](#43-expected-responses)
  - [5. POST: Accept or refuse pending annotation](#5-post-accept-or-refuse-pending-annotation)
    - [5.1. Request body format](#51-request-body-format)
    - [5.2. Example request](#52-example-request)
    - [5.3. Expected responses](#53-expected-responses)
  - [6. GET: Check Rised vehicles from a repertory number](#6-get-check-rised-vehicles-from-a-repertory-number)
    - [6.1. Request query format](#61-request-query-format)
    - [6.2. Example calls](#62-example-calls)
    - [6.3. Expected responses](#63-expected-responses)
  - [7. GET: get owned vehicles by a person](#7-get-get-owned-vehicles-by-a-person)
    - [7.1. Example calls](#71-example-calls)

<!-- licensePlateApplications -->

## 1. GET: Check Vehicle Anotations

`api/vehicles/licensePlates`: for checking whether a vehicle has an annotation in "pending" status.

### 1.1. Request query format

```shell
http://${SERVER_IP}:4031/API/vehicles/licensePlates?patente=VEHICLE_LICENSE_PLATE
```

### 1.2. Example calls

```shell
curl --location --request GET "http://${SERVER_IP}:4031/API/vehicles/licensePlates?patente=BIF-933"
```

### 1.3. Expected responses

Response 200 OK for when there are not pending annotations:

```json
{
    "msg": "sin solicitudes pendientes",
    "success": true
}
```

Response 200 OK for when there is one or more pending annotations for the given plate.

```json
{
    "success": true,
    "solicitudes": [
        {
            "numero_repertorio": "2010-404",    
            "fecha": "2011-11-26T00:00:00.000Z",
            "hora": "23:58:22",  
            "tipo": "AlzPH",     
            "estado": "ingresada"
        }
    ]
}
```

Response 400 BAD REQUEST for when the license plate is invalid (not found in RVM database).

```json
{
    "msg": "invalida",
    "success": false
}
```

<!-- licensePlateCheck -->

## 2. POST: Check if a vehicle exist in the RVM DB

`api/vehicles/licensePlates`: for checking if the given vehicle is registered or not in the RVM database

### 2.1. Request body format

```json
{
    "plate": "Vehicle license plate"
}
```

### 2.2. Example calls

```shell
curl --location --request POST "http://${SERVER_IP}:4031/API/vehicles/licensePlates" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "BIF-933"
    }'
```

### 2.3. Expected responses

Response 200 OK for when the queries plate exists in the RVM database (i.e. is valid):

```json
{
    "valid": true
}
```

Response 200 OK for when the plate does not exist (invalid).

```json
{
    "valid": false
}
```

<!-- ownershipCheck -->

## 3. POST: check ownership of a plate

`api/vehicles/check_ownership`: for checking if a given set of person IDs are a subset or equal to the actual registered owners for the vehicle. This means that, as shown below, `persons` must be an array containing one or more valid owners for the vehicle (with no invalid owners in it).

### 3.1. Request body format

```json
{
    "plate": "Vehicle registration plate",
    "persons": [ "array", "of", "person", "IDs" ]
}
```

### 3.2. Example calls

For any case, if one parameter is missing, the server will reply with 400 BAD REQUEST.

Case 1: license plate and owners are correct (both non case-sensitive). For this case, we pass all the actual owners, which are tree.

Request:

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/check_ownership" \
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
    }'
```

Response 200 OK:

```json
{
    "valid": true
}
```

Case 2: passing a subset of the owners. Like above, but we check that two IDs are owners (not all of them, but yes, they are owners).

Request:

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/check_ownership" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "plate": "BIF-933",
        "owners": [
            "4342908-6",
            "11257169-8"
        ]
    }'
```

Response 200 OK:

```json
{
    "valid": true
}
```

Case 2: invalid license plate, i.e. nonexistent in RVM database (the format is not checked).

Request:

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/check_ownership" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "plate": "BIF-933",
        "owners": [
            "4342908-6",
            "11257169-8",
            "F"
        ]
    }'
```

Response 200 OK:

```json
{
    "valid": false,
    "msg": "Uno o más IDs de dueño son inválidos para el vehiculo"
}
```

<!-- addAnnotations -->

## 4. POST: create new annotation for a plate

`api/vehicles/anotation`: for creating an annotation and link it to a given vehicle.

### 4.1. Request body format

```json
{
    "patente" : "Vehicle registration plate",
    "tipo" : "Annotation type",
    "numero_repertorio" : "Repertory ID e.g. 2010-404"
}
```

### 4.2. Example calls

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/anotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "BIF-933",
        "tipo" : "PN",
        "numero_repertorio" : "2019-54252"
    }'
```

### 4.3. Expected responses

Response 200 OK for when the record was successfully created:

```json
{
    "msg": "Anotacion creada"
}
```

Response 400 BAD REQUEST for when an open annotation already exists for the plate (i.e. in "pending" status, needed to be approved/rejected).

```json
{
    "msg": "Ya hay una anotacion de ese tipo para ese vehiculo, por favor apruebela o rechasela antes de ingresar otra"
}
```

<!-- acceptOrRejectAnnotation -->

## 5. POST: Accept or refuse pending annotation

`api/vehicles/acceptRejectAnotation`: update a pending state annotation (i.e. an existing one in state *'`pendiente`'*) to either *'`aceptado`'* or *'`rechazado`'* for a given vehicle

### 5.1. Request body format

```json
{
    "patente" : "Vehicle registration plate",
    "tipo" : "Annotation Type",
    "aceptarORechazar" : "Update Status (aceptada/rechazada)",
    "numero_repertorio" : "Repertory number"
}
```

### 5.2. Example request

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/acceptRejectAnotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "BIF-933",
        "tipo" : "AlzPN",
        "aceptarORechazar" : "rechazada",
        "numero_repertorio" : "2016-437"
    }'
```

### 5.3. Expected responses

Response 200 OK for when the existing annotation can be successfully updated to accepted/rejected status:

```json
{
    "success": true,
}
```

Response 200 OK for when there is no pending annotation for the given vehicle plate that matches the given type.

```json
{
    "success": false,
    "msg": "No existe una anotacion pendiente de ese tipo para ese vehiculo"
}
```

<!-- develop_repertoryPlactesStatus -->

## 6. GET: Check Rised vehicles from a repertory number

`api/vehicles/currentAnotations`: developing-context endpoint. For checking whether there exist vehicles waiting to be raised. If not, the returns a list of every vehicle associated with one repertory number.

### 6.1. Request query format

```shell
API/vehicles/currentAnotations?numero_repertorio=REPERTORY_NUMBER
```

### 6.2. Example calls

```shell
curl --location --request GET "http://${SERVER_IP}:4031/API/vehicles/currentAnotations?numero_repertorio=2014-316"
```

### 6.3. Expected responses

Response 200 OK with a list of every vehicule asociated with the number repertory number, and a boolean indicating if the vehicule is rised or not.

```json
{
    "msg": "Todos los vehiculos se encuentran alzados",
    "vehicles": "(Lista de patentes)",
    "success": true
}
```


Response 500.

```json
{
    "msg": "Internal Server Error",     
    "error": "Error details"
}
```

<!-- develop_getVehiclesOfPerson -->

## 7. GET: get owned vehicles by a person

Developing-context endpoint, for easily getting the list of vehicles owned by a person, i.e. the vehicles in which the target person is included in the list of owners. The path for this endpoint is:

```txt
API/vehicles/platesOfPerson
```

Response body format:

```json
{
    "plates": "[List<string>] List of license plates in which the target person is [one of] the owners"
}
```

### 7.1. Example calls

Correct request:

```shell
curl --location --request GET "http://${SERVER_IP}:4031/API/vehicles/platesOfPerson?person_id=7900663-7"
```

Response 200 OK, with body:

```json
{
    "plates": [
        "7900663-7",
        "7900663-7"
    ]
}
```

If the `person_id` is not a valid RUN, RUT or passport ID, the `plates` parameter in the response will be an empty list.
