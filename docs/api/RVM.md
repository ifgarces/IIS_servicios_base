# RVM API

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

<!-- TODO: insert table of contents here -->

<!-- TODO: detail path, request/response format and insert example calls for each API method -->

## GET: validate plate

`...`: for checking whether a vehicle exists or not in the RVM database.

## GET: check if a plate has pending annotation(s)

`...`: for checking whether a vehicle has an annotation in "pending" status.

## POST: check ownership of a plate

`api/vehicles/check_ownership`: for checking if a set of person RUNs are the actual registered owners for the vehicle.

### Body format

```json
{
    "plate": "vehicle license plate",
    "persons": [ "array", "of", "person", "IDs" ]
}
```

### Example calls

For any case, if one parameter is missing, the server will reply with 400 BAD REQUEST.

Case 1: license plate and owners are correct (both non case-sensitive).

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

Case 3: passing one or more invalid owners, i.e. not a perfect match for all of them. If even one of them is missing/wrong but the others are OK, it won't be considered valid.

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
    "msg": "Invalid owners"
}
```

## POST: create an annotation for a plate

`...`: for creating an annotation and link it to a given vehicle. The possible annotation types are detailed in the table below.

<!-- TODO: explain each abreviation -->
| Annotation type | Description |
| --------------- | ----------- |
| `"PN"`          | ...         |
| `"PH"`          | ...         |
| `"AlsPN"`       | ...         |
| `"AlsPH"`       | ...         |
| `"CA"`          | ...         |

### Request body format

```json
{
    "plate": "Vehicle license plate",
    "...": "TODO",
    "type": "Annotation type"
}
```

## GET: check a plate has active limitations

`...`: for checking whether the vehicle currently has active limitations (...).
