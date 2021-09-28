# API SRCEI

This API serves the purpose of validating data requests for the SRCEI system ("registro civil"). Let `SERVER_IP` be a shell variable that holds the API server IP address.

## GET: validate person by RUN

`api/users/user`: endpoint to check if user exists or not by passing run as key.

- If user exists: names, last name and run are returned in body.
- If user does not exist: returns body with message that user does not exist.

### Response body format

```json
{
    "userFirstName": "userFirstName",
    "userLastName": "userLastName",
    "userRun": "userRun"
}
```

### Example request

```shell
curl --location --request GET "${SERVER_IP}:4030/api/users/user?run=14343269-6"
```

### Example response (code: 200 OK)

```json
{
    "userFirstName": "LEANDRO ALBERTO",
    "userLastName": "FERRERIA",
    "userRun": "14343269-6"
}
```

## POST: validate person by all data

`api/users`: endpoint that requires the RUN, names, last names and date of birth in the body to validate the user data, as shown below.

### Request body format

```json
{
    "run": "RUN",
    "nombres": "Nombres",
    "apellido_paterno": "Apellido paterno",
    "apellido_materno": "Apellido materno",
    "fecha_nacimiento": "yyyy-MM-dd"
}
```

### Example request

```shell
curl --location --request POST "${SERVER_IP}:4030/api/users/user" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "run": "14343269-6",
        "nombres": "LEANDRO ALBERTO",
        "apellido_paterno": "ferreria",
        "apellido_materno": "CIoBOTARu",
        "fecha_nacimiento": "1992-08-07"
    }'
```

### Example response (code: 200 OK)

```json
{
    "msg": "Usuario existente"
}
```
