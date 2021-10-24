# RVM API

<!-- TODO: finish points 1.1 , 1.2, 3.1, 3.2 -->

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

Every annotation has a type and a status, which possible values are stated in the following tables, respectively.

License plate format: it is composed of three uppercase letters, a hyphen and three numbers as can be seen in the following example (e.g. `"EAM-900"`).

For any call, if there are missing parameters (e.g. in the request query or body), the server will return a response with status 400 BAD REQUEST and a body with a `msg` explaining the reason of the invalid request. When a request triggers an exception in the server, its response will have status 500 and will have this body: `{msg: 'Internal Server Error'}`.

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
    - [3.1. Rquest body format](#31-rquest-body-format)
    - [3.2. Example calls](#32-example-calls)
  - [4. POST: create new annotation for a plate](#4-post-create-new-annotation-for-a-plate)
    - [4.1. Request body format](#41-request-body-format)
    - [4.2 Example calls](#42-example-calls)
    - [4.3 Expected responses](#43-expected-responses)
  - [5. POST: Accept or refuse pending annotation](#5-post-accept-or-refuse-pending-annotation)
    - [5.1. Request body format](#51-request-body-format)
    - [5.2. Example request](#52-example-request)
    - [5.3. Expected responses](#53-expected-responses)

## 1. GET: Check Vehicle Anotations

`api/vehicles/licensePlates`: for checking whether a vehicle has an annotation in "pending" status.

### 1.1. Request query format

```shell
http://${SERVER_IP}:4031/API/vehicles/licensePlates?patente=VEHICLE_LICENSE_PLATE
```

### 1.2. Example calls

```shell
curl --location --request GET "http://${SERVER_IP}:4031/API/vehicles/licensePlates?patente=EAM-900"
```

### 1.3. Expected responses

Response 200 OK for when there are not pending annotations:

```json
{
    "msg": " sin solicitudes pendientes"
}
```

Response 200 OK for when there is one or more pending annotations for the given plate.

```shell
{
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
        "patente" : "EAM-900"
    }'
```

### 2.3. Expected responses

Response 200 OK for when the queries plate exists in the RVM database (i.e. is valid):

```json
{
    "msg": "valida"
}
```

Response 200 OK for when the plate does not exist (invalid).

```json
{
    "msg": "invalida"
}
```

Response 400 BAD REQUEST when the `patente` field is missing.

```json
{
    "msg": "Es necesaria la patente"
}
```

## 3. POST: check ownership of a plate

`api/vehicles/check_ownership`: for checking if a given set of person IDs are a subset or equal to the actual registered owners for the vehicle. This means that, as shown below, `persons` must be an array containing one or more valid owners for the vehicle (with no invalid owners in it).

### 3.1. Rquest body format

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
        "plate": "LEC-681",
        "owners": [
            "4930477-3",
            "10651736-3",
            "14652074-K"
        ]
    }'
```

Response 200 OK:

```json
{
    "msg": "Valid"
}
```

Case 2: passing a subset of the owners. Like above, but we check that two IDs are owners (not all of them, but yes, they are owners).

Request:

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/check_ownership" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "plate": "LEC-681",
        "owners": [
            "4930477-3",
            "10651736-3"
        ]
    }'
```

Response 200 OK:

```json
{
    "msg": "Valid"
}
```

Case 2: invalid license plate, i.e. nonexistent in RVM database (the format is not checked).

Request:

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/check_ownership" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "plate": "GOW por fin en PC en enero",
        "owners": [
            "4930477-3",
            "10651736-3",
            "14652074-K"
        ]
    }'
```

Response 200 OK:

```json
{
    "msg": "Invalid plate"
}
```

## 4. POST: create new annotation for a plate

`api/vehicles/anotation`: for creating an annotation and link it to a given vehicle.

### 4.1. Request body format

```json
{
    "patente" : "Vehicle registration plate",
    "tipo" : "Annotation type",
    "numero_repertorio" : "Repertory Number"
}
```

### 4.2 Example calls

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/anotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PN",
        "numero_repertorio" : "0001"
    }'
```

### 4.3 Expected responses

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

Response 400 BAD REQUEST for when the `tipo` field does not match any string from table 1:

```json
{
    "msg": "Es necesario el tipo de anotacion ('PN', 'PH', 'AlzPN', 'AlzPH', 'CA')"
}
```

## 5. POST: Accept or refuse pending annotation

`api/vehicles/acceptRejectAnotation`: update a pending state annotation (i.e. an existing one in state *'`pendiente`'*) to either *'`aceptado`'* or *'`rechazado`'* for a given vehicle

### 5.1. Request body format

```json
{
    "patente" : "Vehicle registration plate",
    "tipo" : "Annotation Type",
    "aceptarORechazar" : "Update Status (aceptada/rechazada)"
}
```

### 5.2. Example request

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/acceptRejectAnotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PH",
        "aceptarORechazar" : "rechazada"
    }'
```

### 5.3. Expected responses

Response 200 OK for when the existing annotation can be successfully accepted/rejected:

```json
{
    "msg": "Anotacion actualizada"
}
```

Response 400 BAD REQUEST for when the `tipo` field does not match any string from table 1:

```json
{
    "msg": "Es necesario el tipo de anotacion ('PN', 'PH', 'AlzPN', 'AlzPH', 'CA')"
}
```
