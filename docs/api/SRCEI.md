# API SRCEI

This API serves the purpose of validating data requests for the SRCEI.

## GET: Validate User
## ec2-54-90-219-192.compute-1.amazonaws.com:4030/api/users/user

Endpoint to check if user exists or not by pasing run as key
- If user does exist: names, lastname and run are returned in body.
- If user does not exist: returns body with message that user does not exist.

### Response Body:
```
{
    "userFirstName": "userFirstName",
    "userLastName": "userLastName",
    "userRun": "userRun"
}
```
### Example Request
```
curl --location --request GET 'http://ec2-54-90-219-192.compute-1.amazonaws.com:4030/api/users/user?run=14343269-6'
```
### Example Response (Code: 200 OK)
```
{
    "userFirstName": "LEANDRO ALBERTO",
    "userLastName": "FERRERIA",
    "userRun": "14343269-6"
}
```

## POST: Validate User Data
## ec2-54-90-219-192.compute-1.amazonaws.com:4030/api/users

Endpoint that requires the run, names, lastname1, lastname2, and date of birth in the body to validate the user data.

### Body:
```
{
    "run": "run",
    "nombres": "Nombres",
    "apellido_paterno": "Apellido_paterno",
    "apellido_materno": "Apellido_materno",
    "fecha_nacimiento": "yyyy-mm-dd"
}
```
### Example Request
```
curl --location --request POST 'http://ec2-54-90-219-192.compute-1.amazonaws.com:4030/api/users/user'
--data-raw '{
    "run": "14343269-6",
    "nombres": "LEANDRO ALBERTO",
    "apellido_paterno": "FERRERIA",
    "apellido_materno": "CIOBOTARU",
    "fecha_nacimiento": "1992-08-07"
}'
```
### Example Response (Code: 200 OK)
```
{
    "msg": "Usuario existente"
}
```