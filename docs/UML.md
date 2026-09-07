# UML and Architecture Notes

## Use case

```mermaid
flowchart LR
  Admin --> Login
  Student --> Login
  Admin --> ManageUsers
  Student --> Transcript
  Student --> Invoice
  Admin --> Payroll
  Login --> Gateway
  Transcript --> Academic
  Invoice --> Finance
  Payroll --> HR
```

## Deployment

```mermaid
flowchart LR
  Client --> Gateway
  Gateway --> Auth
  Gateway --> Academic
  Gateway --> Finance
  Gateway --> HR
  Auth --> MySQL
  Academic -. enrollment event .-> RabbitMQ
  RabbitMQ -. invoice consumer .-> Finance
```

## Enrollment sequence

```mermaid
sequenceDiagram
  participant Client
  participant Gateway
  participant Academic
  participant Broker as RabbitMQ
  participant Finance
  Client->>Gateway: POST enrollment
  Gateway->>Academic: validate and save enrollment
  Academic->>Broker: publish StudentEnrolled
  Academic-->>Gateway: 202 Accepted
  Broker->>Finance: deliver event
  Finance->>Finance: create invoice
```

## Class model

The service request models are the code-level classes: `RegisterRequest`, `LoginRequest`, `Grade`, `TranscriptRequest`, `InvoiceRequest`, and `PayrollRequest`. Each service owns its model and persistence boundary.
