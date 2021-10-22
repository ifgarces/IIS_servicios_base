# PPE API

This API serves the purpose of validating data requests for the PPE system (*portal de pago electrónico*). Note that this system is supposed to interact asynchronously with TGR (*tesorería general de la república*) for payment confirmation, which will be simulated (see the section below).

<!-- TODO: insert table of contents here -->

## Confirmation from TGR

When receiving a valid payment call from the PPE API consumer (Prendas), the transaction is registered and marked as pending (from TGR confirmation), and the ID for that transaction is returned to Prendas in the response immediately. Then, a random amount of time is set for the simulated TGR to send the confirmation to Prendas (passing the transaction ID previously returned to Prendas by PPE), by consuming an API exposed by Prendas after that random time. See the image below. There's also a probability for TGR to never send the confirmation, which has to be considered (Prendas will have to set a timeout for TGR confirmation for a PPE transaction).

![PPE payment flow](./diagram_PPE_payment_flow.jpg "PPE payment flow diagram")

## 1. POST: register payment attempt (PPE)

`api/transaction/payment`: endpoint that immediately register the payment in PPE and returns the transaction ID, and starts the simulated TGR response flow. It requieres the person id, repertoire number and the amount of money.

### 1.1. Request body format

```json
{
    "id_persona": "Person ID",
    "numero_repertorio": "N°Repertoire",
    "monto": "Amount"
}
```

### 1.2. Example calls

Request:

```shell
curl --location --request POST "${SERVER_IP}:4032/api/transaction/payment" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "id_persona": "1092093-5",
        "numero_repertorio": "123",
        "monto": 213540
    }'
```

Response 200 OK:

```json
{
    "msg": "Pago Ingresado"
}
```

Note: if a body parameter is missing, an exception will be triggered in the server.

## 2. POST: confirm payment (TGR)

This endpoint is consumed by ourselves and has to be exposed by the Prendas systems. Once we have it, this works as a callback from the payment attempt API endpoint.

The documentation for this endpoint has to be provided from Prendas.
