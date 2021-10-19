# RVM API

This API serves the purpose of validating data requests for the RVM system (*registro de vehículos motorizados*).

<!-- TODO: insert table of contents here -->

<!-- TODO: detail path, request/response format and insert example calls for each API method -->

## GET: validate plate

`...`: for checking whether a vehicle exists or not in the RVM database.

## GET: check if a plate has pending annotation(s)

`...`: for checking whether a vehicle has an annotation in "pending" status.

## GET: check ownership of a plate

`...`: for checking if a set of person RUNs are the actual registered owners for the vehicle.

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
