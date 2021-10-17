# PPE API

This API serves the purpose of validating data requests for the PPE system (*portal de pago electrónico*). Note that this system is supposed to interact asynchronously with TGR (*tesorería general de la república*) for payment confirmation, which will be simulated (see the section below).

<!-- TODO: insert table of contents here -->

## Confirmation from TGR

When receiving a valid payment call from the PPE API consumer (Prendas), the transaction is registered and marked as pending (from TGR confirmation), and the ID for that transaction is returned to Prendas in the response immediately. Then, a random amount of time is set for the simulated TGR to send the confirmation to Prendas (passing the transaction ID previously returned to Prendas by PPE), by consuming an API exposed by Prendas after that random time. There's also a probability for TGR to never send the confirmation, which has to be considered (Prendas will have to set a timeout for TGR confirmation for a PPE transaction).

<!-- TODO: insert diagram explaining the PPE-TGR-Prendas flow -->

## ...

<!-- TODO: explain all calls, insert example request-response for various scenarios -->
