# Caja API

This API serves the purpose of processing checkout (*caja*) system transactions.

- [Caja API](#caja-api)
  - [1. POST: process payment](#1-post-process-payment)
    - [1.1. Request body format](#11-request-body-format)
    - [1.2. Example calls](#12-example-calls)
  - [2. POST: process refund](#2-post-process-refund)
    - [2.1. Request body format](#21-request-body-format)
    - [2.2. Example calls](#22-example-calls)

## 1. POST: process payment

`api/checkout/pay`: for registering a payment.

### 1.1. Request body format

```json
{
    "RUN" : "personRUN",
    "monto" : "paymentAmount"
}
```

### 1.2. Example calls

For a correct payment call:

Request:

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/pay" \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "RUN" : "16248093-6",
    "monto" : "22700"
}'
```

Response 200 OK:

```json
{
    "msg": "Monto Ingresado"
}
```

For an incorrect payment call:

Request:

TODO <!-- TODO: wrong request -->

Response: <!-- TODO: expected response code -->

TODO <!-- TODO: error response -->

## 2. POST: process refund

`api/refund`: for registering a refund.

### 2.1. Request body format

```json
{
    "RUN" : "personRUN",
    "monto" : "paymentAmount"
}
```

### 2.2. Example calls

For a correct refund call: <!-- TODO: should reference ID of a previous payment -->

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/refund" \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "RUN" : "16248093-6",
    "monto" : "21821.74"
}'
```

Response 200 OK:

```json
{
    "msg": "Monto Retirado"
}
```
