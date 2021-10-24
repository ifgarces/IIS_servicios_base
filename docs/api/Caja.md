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
    "id_persona" : "identificador_persona (string)",
    "numero_repertorio" : "identificador_prenda (integer)",
    "monto" : "monto_a_pagar (decimal)"
}
```

Only one payment per "numero_repertorio". (En caso de duda preguntar)

### 1.2. Example calls

For a correct payment call:

Request:

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/pay" \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "numero_repertorio" : "1234",
    "id_persona" : "16248093-6",
    "monto" : "22.5"
}'
```

Response 200 OK:

```json
{
    "msg": "Monto Ingresado",
    "nuevo_folio": 51
}
```

If there are missing or wrong body parameters, the server will trigger an exception and return a status 500 response, like follows.

```json
{
    "msg" : "Internal Server Error"
}
```

## 2. POST: process refund

`api/checkout/refund`: for registering a refund.

You can only request a refund for an existing payment.

### 2.1. Request body format

```json
{
    "folio": "identificador_transacción (integer)",
    "id_persona": "identificador_persona (string)",
    "numero_repertorio": "identificador_prenda (integer)"
}
```

### 2.2. Example calls

For a correct refund call:

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/refund" \
    --header 'Content-Type: application/json' \
    --data-raw '{ 
    "folio":31,
    "id_persona" : "11149472-K",
    "numero_repertorio" : 31
}'
```

Response 200 OK:

```json
{
    "msg": "Monto Reembolsado",
    "nuevo_folio": 51
}
```

Response 400:

```json
{
    "msg" : "No existen Pagos para los parametros ingresados"
}
```

Response 401:

```json
{
    "msg" : "Reembolso denegado"
}
```

Response 500:

```json
{
    "msg" : "Internal Server Error"
}
```
