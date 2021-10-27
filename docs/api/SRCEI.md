# SRCEI API

This API serves the purpose of validating data requests for the SRCEI system (*registro civil*).

- [SRCEI API](#srcei-api)
  - [1. GET: validate person by RUN and get full name](#1-get-validate-person-by-run-and-get-full-name)
    - [1.1. Response body format](#11-response-body-format)
    - [1.2. Example calls](#12-example-calls)
  - [2. POST: validate person by all data](#2-post-validate-person-by-all-data)
    - [2.1. Request body format](#21-request-body-format)
    - [2.2. Example calls](#22-example-calls)

<!-- simpleCheck -->

## 1. GET: validate person by RUN and get full name

`api/users/user`: endpoint to check if user exists or not by passing run as key.

- If user exists: names, last name and run are returned in body.
- If user does not exist: returns body with message that user does not exist.

### 1.1. Response body format

```json
{
    "nombres": "PERSON NAME(S)",
    "apellido_paterno": "PERSON FIRST LAST NAME",
    "apellido_materno": "PERSON SECOND LAST NAME"
}
```

### 1.2. Example calls

For the scenario in which we query for a valid person RUN:

Request:

```shell
curl --location --request GET "${SERVER_IP}:4030/api/users/user?run=14343269-6"
```

Response 200 OK:

```json
{
    "nombres": "LEANDRO ALBERTO",
    "apellido_paterno": "FERRERIA",
    "apellido_materno": "CIOBOTARU"
}
```

If we query for an invalid person RUN (i.e. one that does not exist in the SRCEI database):

Request:

```shell
curl --location --request GET "localhost:4030/api/users/user?run=14343269-k"
```

Response 200 OK:

```json
{
  "msg": "RUN inválido: no registrado"
}
```

Note that this result will be the same for not valid RUTs, for example, for `curl --location --request GET "localhost:4030/api/users/user?run=empanada"`.

If the `run` query parameter is not provided, the server will return with a 400 BAD REQUEST response, explaining the error.

<!-- strictCheck -->

## 2. POST: validate person by all data

`api/users`: endpoint that requires the RUN, names, last names and date of birth in the body to validate the user data, as shown below.

### 2.1. Request body format

```json
{
    "run": "RUN",
    "nombres": "Nombres",
    "apellido_paterno": "Apellido paterno",
    "apellido_materno": "Apellido materno"
}
```

### 2.2. Example calls

Names and lastnames are not case-sensitive. If we query for an existing person with the right data:

Request:

```shell
curl --location --request POST "${SERVER_IP}:4030/api/users/user" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "run": "14343269-6",
        "nombres": "LEANDRO ALBERTO",
        "apellido_paterno": "ferreria",
        "apellido_materno": "CIoBOTARu"
    }'
```

Response 200 OK:

```json
{
    "msg": "Usuario existente"
}
```

When the passed data is not valid (i.e. when the RUN is invalid or the person data does not match in all of the fields):

Request:

```shell
curl --location --request POST "${SERVER_IP}:4030/api/users/user" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "run": "14343269-6",
        "nombres": "LEANDRO ALBERTO",
        "apellido_paterno": "ferreria",
        "apellido_materno": "CIoBOTARu"
    }'
```

Response 200 OK:

```json
{
    "msg": "Usuario no existe"
}
```

The same result will be obtained if another field (non-case sensitive) does not match exactly with the SRCEI database entry for that person.

Note: if a body parameter is missing, an exception will be triggered in the server.
