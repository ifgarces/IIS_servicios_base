# RVM API

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

- [RVM API](#rvm-api)
  - [1. GET: validate plate](#1-get-validate-plate)
    - [1.1. Example calls](#11-example-calls)
  - [2. GET: check if a plate has pending annotation(s)](#2-get-check-if-a-plate-has-pending-annotations)
    - [2.1. Example calls](#21-example-calls)
  - [3. GET: check a plate has active annotation(s)](#3-get-check-a-plate-has-active-annotations)
    - [3.1. Example calls](#31-example-calls)
  - [4. POST: check ownership of a plate](#4-post-check-ownership-of-a-plate)
    - [4.1. Body format](#41-body-format)
    - [4.2. Example calls](#42-example-calls)
  - [5. POST: create an annotation for a plate](#5-post-create-an-annotation-for-a-plate)
    - [5.1. Request body format](#51-request-body-format)

<!-- TODO: detail path, request/response format and insert example calls for each API method -->

## 1. GET: validate plate

`...`: for checking whether a vehicle exists or not in the RVM database.

### 1.1. Example calls

TODO <!-- TODO -->

## 2. GET: check if a plate has pending annotation(s)

`...`: for checking whether a vehicle has an annotation in "pending" status.

### 2.1. Example calls

TODO <!-- TODO -->

## 3. GET: check a plate has active annotation(s)

`...`: for checking whether the vehicle currently has active limitations (...).

### 3.1. Example calls

TODO <!-- TODO -->

## 4. POST: check ownership of a plate

`api/vehicles/check_ownership`: for checking if a given set of person IDs are a subset or equal to the actual registered owners for the vehicle. This means that, as shown below, `persons` must be an array containing one or more valid owners for the vehicle (with no invalid owners in it).

### 4.1. Body format

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

## 5. POST: create an annotation for a plate

`...`: for creating an annotation and link it to a given vehicle. The possible annotation types are detailed in the table below.

<!-- TODO: explain each abreviation -->
| Annotation type | Description |
| --------------- | ----------- |
| `"PN"`          | `Prenda`         |
| `"PH"`          | `Prohibicion`         |
| `"AlzPN"`       | `Alzamiento Prenda`         |
| `"AlzPH"`       | `Alzamiento Prohibicion`         |
| `"CA"`          | `Cambio Acreedor`         |

### 5.1. Request body format

```json
{
    "plate": "Vehicle license plate",
    "...": "TODO",
    "type": "Annotation type"
}
```
## 6. POST: Create a new annotation

<!-- TODO: add success or error examples -->
### Request body format

```json
{
    "plate": "Vehicle license plate",
    "...": "TODO",
    "type": "Annotation type"
}
```

### 6.1 Example request

```shell
curl --location --request POST " http://${SERVER_IP}:4031/API/vehicles/anotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PN",
        "numero_repertorio" : "0001"
    }'
```

## 7. POST: Accept or refuse pending anotation

<!-- TODO: add success or error examples -->
### Request body format

```json
{
    "plate": "Vehicle license plate",
    "...": "TODO",
    "type": "Annotation type"
}
```

### 7.1 Example request

```shell
curl --location --request POST "http://${SERVER_IP}:4031/API/vehicles/anotation" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PH",
        "aceptarORechazar" : "rechazada"
    }'
```

## 8. POST: Check if vehicle has pending anotation
<!-- TODO: add success or error examples -->
### Request body format

```json
{
    "plate": "Vehicle license plate",
    "...": "TODO",
    "type": "Annotation type"
}
```

### Check if vehicle has pending anotation

```shell
curl --location --request POST "http://${SERVER_IP}:4031/API/vehicles/checkAnotacion" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "patente" : "EAM-900",
        "tipo" : "PN"
    }'
```
