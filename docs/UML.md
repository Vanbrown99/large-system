# UML and Architecture Notes

## Use-Case Diagram

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

## Class Diagram

```mermaid
classDiagram
  class User { +id: bigint +name: string +email: string +password_hash: string +role: string }
  class Student { +id: bigint +student_number: string +programme: string }
  class Course { +id: bigint +code: string +name: string +credit_units: int }
  class Grade { +id: bigint +score: decimal }
  class AcademicTranscript { +id: bigint +student_id: string +average_score: decimal +credits: int +standing: string }
  class TranscriptGrade { +id: bigint +course_code: string +score: decimal +credit_units: int }
  class AcademicEnrollment { +id: bigint +student_id: string +tuition: decimal }
  class FinanceInvoice { +id: bigint +student_id: string +amount: decimal +status: string }
  class Payroll { +id: bigint +employee_id: string +gross_salary: decimal +net_salary: decimal }
  User "1" --> "0..1" Student
  Student "1" --> "*" Grade
  Course "1" --> "*" Grade
  AcademicTranscript "1" --> "*" TranscriptGrade
```

## ERD - Academic Module

```mermaid
erDiagram
  USERS ||--o| STUDENTS : owns
  STUDENTS ||--o{ GRADES : receives
  COURSES ||--o{ GRADES : records
  ACADEMIC_TRANSCRIPTS ||--o{ ACADEMIC_TRANSCRIPT_GRADES : contains
  USERS { bigint id PK string email UK string password_hash string role }
  STUDENTS { bigint id PK bigint user_id FK string student_number UK string programme }
  COURSES { bigint id PK string code UK string name int credit_units }
  GRADES { bigint id PK bigint student_id FK bigint course_id FK decimal score }
  ACADEMIC_TRANSCRIPTS { bigint id PK string student_id decimal average_score int credits string standing }
  ACADEMIC_TRANSCRIPT_GRADES { bigint id PK bigint transcript_id FK string course_code decimal score int credit_units }
  ACADEMIC_ENROLLMENTS { bigint id PK string student_id decimal tuition decimal accommodation decimal other_fees }
```

## ERD - Finance Module

```mermaid
erDiagram
  FINANCE_INVOICES { bigint id PK string student_id decimal amount string status datetime created_at }
```

## ERD - HR Module

```mermaid
erDiagram
  HR_PAYROLL { bigint id PK string employee_id decimal gross_salary decimal pension decimal tax decimal net_salary datetime created_at }
```

## Deployment Diagram

```mermaid
flowchart LR
  Client --> Gateway
  Gateway --> Auth
  Gateway --> Academic: JWT validated
  Gateway --> Finance: JWT validated
  Gateway --> HR: JWT validated
  Auth --> MySQL
  Academic -. enrollment event .-> RabbitMQ
  RabbitMQ -. invoice consumer .-> Finance
```

## Enrollment Sequence Diagram

```mermaid
sequenceDiagram
  participant Client
  participant Gateway
  participant Academic
  participant Broker as RabbitMQ
  participant Finance
  Client->>Gateway: POST enrollment
  Gateway->>Gateway: validate JWT
  Gateway->>Academic: validate and save enrollment
  Academic->>Broker: publish StudentEnrolled
  Academic-->>Gateway: 202 Accepted
  Broker->>Finance: deliver event
  Finance->>Finance: create invoice
```

The request model classes `RegisterRequest`, `LoginRequest`, `Grade`, `TranscriptRequest`, `InvoiceRequest`, and `PayrollRequest` validate each API request before persistence or processing.
