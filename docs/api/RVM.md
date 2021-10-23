# RVM API

<!-- TODO: finish points 1.1 , 1.2, 3.1, 3.2 -->

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

Every reference made to an annotations uses either the Type or Status. On the tables show below are listed the different values for each one of the keys.

| Annotation type | Description |
| --------------- | ----------- |
| `"PN"`          | `Prenda`         |
| `"PH"`          | `Prohibicion`         |
| `"AlzPN"`       | `Alzamiento Prenda`         |
| `"AlzPH"`       | `Alzamiento Prohibicion`         |
| `"CA"`          | `Cambio Acreedor`         |


| Annotation status | Description |
| ----------------- | ----------- |
| `"ingresada"`     | `Anotacion en estado ingresada`|
| `"aceptada"`      | `Anotacion en estado aceptado` |
| `"rechazada"`     | `Anotacion en estado rechazado`|


- [RVM API](#rvm-api)
  - [1. GET: Check Vehicle Anotations](#1-get-check-vehicle-anotations)
    - [1.1. Request body format](#11-request-body-format)
    - [1.2. Example calls](#12-example-calls)
    - [1.3. Expected response](#13-expected-response)
  - [2. GET: check if a plate has pending annotation(s)](#2-get-check-if-a-plate-has-pending-annotations)
    - [2.1. Request body format](#21-request-body-format)
    - [2.2. Example calls](#22-example-calls)
    - [2.3. Expected response](#23-expected-response)
  - [3. POST: Check if a vehicle exist in the RVM DB](#3-post-check-if-a-vehicle-exist-in-the-rvm-db)
    - [3.1. Request body format](#31-request-body-format)
    - [3.2. Example calls](#32-example-calls)
    - [3.3. Expected response](#33-expected-response)
  - [4. POST: check ownership of a plate](#4-post-check-ownership-of-a-plate)
    - [4.1. Rquest body format](#41-rquest-body-format)
    - [4.2. Example calls](#42-example-calls)
    - [4.3. Expected Response](#43-expected-response)
  - [5. POST: create new annotation for a plate](#5-post-create-new-annotation-for-a-plate)
    - [5.1. Request body format](#51-request-body-format)
    - [5.2 Example calls](#52-example-calls)
    - [5.3 Expected Response](#53-expected-response)
  - [6. POST: Accept or refuse pending anotation](#6-post-accept-or-refuse-pending-anotation)
    - [6.1. Request body format](#61-request-body-format)
    - [6.2. Example request](#62-example-request)
    - [6.3. Expected response](#63-expected-response)


## 1. GET: Check Vehicle Anotations

`api/vehicles/licensePlates`: for recieving the list of applications in state '`pending`' for a given vehicle

### 1.1. Request body format

### 1.2. Example calls

### 1.3. Expected response
Response 200 OK:

- The requeted plate does not have any pending application
```json
{
    "msg": "sin solicitudes pendientes"
}
```

- The requeted plate does not exists in the RVM DB
```json
{
    "msg": "invalida"
}
```
- If the plate has pending applications, the call will return the list of pending applications


Response 401 Unauthorized:

- If body is missing key *'`patente`'*
```json
{
    "msg": "Es necesaria la patente SOLICITUDES"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error 2"
}
```


## 2. GET: check if a plate has pending annotation(s)

`api/vehicles/checkAnotacion`: for checking whether a vehicle has an annotation in "pending" status of a given annotation type.

### 2.1. Request body format

```json
{
    "patente": "Vehicle license plate",
    "tipo": "Annotation type"
}
```

### 2.2. Example calls

```shell
curl --location --request POST "http://${SERVER_IP}:4031/API/vehicles/checkAnotacion" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PN"
    }'
```

### 2.3. Expected response

Response 200 OK:


```json
{
    "msg": "Anotacion pendiente de este tipo para este vehiculo"
}
```


```json
{
    "msg": "No hay anotaciones pendientes de este tipo para este vehiculo"
}
```

Response 401 Unauthorized:

If body is missing key *'patente'*
```json
{
    "msg": "Falta ingresar patente"
}
```

If body is missing key *'tipo'* of annotation
```json
{
    "msg": "Es necesario el tipo de anotacion ('PN', 'PH', 'AlzPN', 'AlzPH', 'CA')"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error 1"
}
```


## 3. POST: Check if a vehicle exist in the RVM DB

`api/vehicles/licensePlates`: for checking if the given vehicle is registered or not in the RVM database

### 3.1. Request body format

### 3.2. Example calls

### 3.3. Expected response

Response 200 OK:

- The queried plate exist in the RVM DB
```json
{
    "msg": "valida"
}
```

- The queried plate does not exist in the RVM DB
```json
{
    "msg": "invalida"
}
```

Response 401 Unauthorized:

- If body is missing key *'`patente`'*
```json
{
    "msg": "Es necesaria la patente"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error 2"
}
```


## 4. POST: check ownership of a plate

`api/vehicles/check_ownership`: for checking if a given set of person IDs are a subset or equal to the actual registered owners for the vehicle. This means that, as shown below, `persons` must be an array containing one or more valid owners for the vehicle (with no invalid owners in it).

### 4.1. Rquest body format

```json
{
    "plate": "vehicle license plate",
    "persons": [ "array", "of", "person", "IDs" ]
}
```

### 4.2. Example calls

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

### 4.3. Expected Response

Response 200 OK:

- Valid array of owners for a given vehicle
```json
{
    "msg": "Valid"
}
```

- The plate is not valid in the RVM Data Base
```json
{
    "msg": "Invalid plate"
}
```

- The array of owners provided do not include a valid owner of the vehicle
```json
{
    "msg": "Invalid owners"
}
```

Response 400 Bad Request:

- If body is either missing key *'`plate`'* or key *'`owners`'*
```json
{
    "msg": "One of 'plate' or 'owners' parameters missing or empty"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error"
}
```


## 5. POST: create new annotation for a plate

`api/vehicles/anotation`: for creating an annotation and link it to a given vehicle. 

### 5.1. Request body format


```json
{
    "patente" : "Vehicle license plate",
    "tipo" : "Annotation type",
    "numero_repertorio" : "Repertory Number"
}
```

### 5.2 Example calls

```shell
curl --location --request POST " http://${SERVER_IP}:4031/api/vehicles/anotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PN",
        "numero_repertorio" : "0001"
    }'
```

### 5.3 Expected Response 

Response 200 OK:

- On a successful creation
```json
{
    "msg": "Anotacion creada"
}
```

Response 401 Unauthorized:

- If body is missing key *'`patente`'*
```json
{
    "msg": "Falta ingresar patente"
}
```

- If body is missing key *'`tipo`'* of annotation
```json
{
    "msg": "Es necesario el tipo de anotacion ('PN', 'PH', 'AlzPN', 'AlzPH', 'CA')"
}
```

- If body is missing key *'`numero_repertorio`'*
```json
{
    "msg": "Falta numero de repertorio"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error"
}
```

## 6. POST: Accept or refuse pending anotation

`api/vehicles//acceptRejectAnotation`:update a pending state annotation to either *'`aceptado`'* or *'`rechazado`'* for a given vehicle

### 6.1. Request body format

```json
{
    "patente" : "Vehicle License Plate",
    "tipo" : "Annotation Type",
    "aceptarORechazar" : "Update Status (aceptada/rechazada)"
}
```

### 6.2. Example request

```shell
curl --location --request POST "http://${SERVER_IP}:4031/api/vehicles/acceptRejectAnotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PH",
        "aceptarORechazar" : "rechazada"
    }'
```

### 6.3. Expected response
Response 200 OK:

- On a successful actualization
```json
{
    "msg": "Anotacion actualizada"
}
```

Response 401 Unauthorized:

- If body is missing key *'`patente`'*
```json
{
    "msg": "Falta ingresar patente"
}
```

- If body is missing key *'`tipo`'* of annotation
```json
{
    "msg": "Es necesario el tipo de anotacion ('PN', 'PH', 'AlzPN', 'AlzPH', 'CA')"
}
```

- If body is missing key *'`aceptarORechazar`'*
```json
{
    "msg": "Falta elejir si se esta 'aceptada' o 'rechazada' la anotacion"
}
```

Respones 500 Internal Server Error:

```json
{
    "msg": "Internal Server Error 2"
}
```
