# Caja API

This API serves the purpose of processing checkout (*caja*) system transactions.

- [Caja API](#caja-api)
  - [1. POST: process payment](#1-post-process-payment)
    - [1.1. Request body format](#11-request-body-format)
    - [1.2. Example calls](#12-example-calls)
  - [2. POST: process refund](#2-post-process-refund)
    - [2.1. Request body format](#21-request-body-format)
    - [2.2. Example calls](#22-example-calls)

<!-- manualCreatePayment -->

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
    "numero_repertorio" : "101-A",
    "id_persona" : "16248093-6",
    "monto" : 22
}'
```

Response 200 OK:

```json
{
    "msg": "Monto Ingresado",
    "success": true,
    "nuevo_folio": 51
}
```

<!-- manualPaymentRefund -->

## 2. POST: process refund

`api/checkout/refund`: for registering a refund.

You can only request a refund for an existing payment.

### 2.1. Request body format

```json
{
    "id_persona": "identificador_persona (string)",
    "numero_repertorio": "identificador_prenda (integer)",
    "folio_ingreso": "indentificador_pago (integer)"
}
```

### 2.2. Example calls

For a correct refund call:

```shell
curl --location --request POST "${SERVER_IP}:4033/api/checkout/refund" \
    --header 'Content-Type: application/json' \
    --data-raw '{ 
    "id_persona" : "11149472-K",
    "numero_repertorio" : "310-A",
    "folio_ingreso": 31
}'
```

Response 200 OK:

```json
{
    "success": true,
    "msg": "Monto Reembolsado",
    "nuevo_folio": 51
}
```

Response 200 OK:

```json
{
    "success": false,
    "msg" : "No existen Pagos para los parametros ingresados"
}
```

Response 200 OK:

```json
{
    "success": false,
    "msg" : "Reembolso denegado, no existen pagos en registro"
}
```

Response 200 OK:

```json
{
    "success": false,
    "msg" : "Reembolso denegado"
}
```
