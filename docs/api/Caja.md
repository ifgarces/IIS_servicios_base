# API CAJA

This API serves the purpose of processing checkout ("caja") system transactions. Let `SERVER_IP` be a shell variable that holds the API server IP address.

## POST: process payment

`api/checkout/pay`: for registering a payment.

### Request body format

```json
{
    "RUN" : "personRUN",
    "fecha" : "yyyy-MM-dd",
    "monto" : "paymentAmount"
}
```

### Example request

```shell
curl --location --request GET "${SERVER_IP}:4033/api/checkout/pay" --data-raw '{
    "RUN" : "19245093-8",
    "fecha" : "2021-03-5",
    "monto" : "22700"
}'
```

### Example response (code: 200 OK)

```json
{
    "msg": "Monto Ingresado"
}
```

## POST: process refund

`api/refound`: for registering a refund.

### Request body format

```json
{
    "RUN" : "personRUN",
    "fecha" : "yyyy-MM-dd",
    "monto" : "paymentAmount"
}
```

### Example request

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/refund" --data-raw '{
    "RUN" : "16248093-6",
    "fecha" : "2005-10-31",
    "monto" : "21821.74"
}'
```

### Example response (code: 200 OK)

```json
{
    "msg": "Monto Retirado"
}
```
