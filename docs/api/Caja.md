# API CAJA

This API serves the purpose of validating data requests for the CAJA.

## POST: Process Payment
## localhost:4033/api/checkout/pay

### Body:
```
{
    "RUN" : "userRun",
    "fecha" : "yyyy-mm-dd",
    "monto" : "paymentAmount"
}
```

### Example Request
```
curl --location --request GET 'localhost:4033/api/checkout/pay'
api/checkout/refund'
--data-raw '{
    "RUN" : "19245093-8",
    "fecha" : "2021-03-5",
    "monto" : "22700"
}'
```
### Example Response (Code: 200 OK)
```
{
    "msg": "Monto Ingresado"
}
```

## POST: Process Refund
## localhost:4033/api/refound

### Body:
```
{
    "RUN" : "userRun",
    "fecha" : "yyyy-mm-dd",
    "monto" : "paymentAmount"
}
```
### Example Request
```
curl --location --request POST 'localhost:4033/api/checkout/refund'
--data-raw '{
    "RUN" : "16248093-6",
    "fecha" : "2005-10-31",
    "monto" : "21821.74"
}'
```
### Example Response (Code: 200 OK)
```
{
    "msg": "Monto Retirado"
}
```