<!-- TODO: API endpoints with examples (`curl` commands and expected result) -->

# API SRCEI

This API serves the purpose of validating data requests for the CAJA.

## POST: Generate Payment
## ec2-54-90-219-192.compute-1.amazonaws.com:4034/api/checkout/pay

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
curl --location --request GET 'http://ec2-54-90-219-192.compute-1.amazonaws.com:4034/api/checkout/pay'
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

## POST: Generate Refund
## ec2-54-90-219-192.compute-1.amazonaws.com:4033/api/

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
curl --location --request POST 'http://ec2-54-90-219-192.compute-1.amazonaws.com:4034/api/checkout/refund'
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