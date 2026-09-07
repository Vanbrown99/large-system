# School ERP Microservices

SEN4121 Large System Environment practical project. The platform is organized around an API Gateway and four independently deployable services.

## Run the whole system

Prerequisite: Docker Desktop.

```powershell
docker compose up --build
```

OpenAPI documentation is available at:

- Gateway: http://localhost:8000/docs
- Auth service: http://localhost:8001/docs when port exposure is added for isolated demo

## Demonstration journey

1. Register an admin and a student through `POST /api/v1/auth/register`.
2. Log in through `POST /api/v1/auth/login` and copy the bearer token.
3. Call `POST /api/v1/academic/transcripts` to generate a transcript.
4. Call `POST /api/v1/finance/invoices` to generate an invoice.
5. Call `POST /api/v1/hr/payroll` to calculate payroll deductions.
6. Send 11 requests in one minute from one client to demonstrate the gateway's `429` response.
7. Call `POST /api/v1/academic/enrollments` and then `GET /api/v1/finance/invoices/{student_id}` to demonstrate the RabbitMQ `StudentEnrolled` event creating an invoice asynchronously.

## Quality evidence

- Passwords are bcrypt hashes; plaintext passwords are never stored.
- JWTs carry the user subject, role, and expiration.
- The gateway is the public entry point and applies a per-client rate limit.
- Academic publishes durable `StudentEnrolled` events to RabbitMQ; Finance consumes them and creates invoices asynchronously.
- `database/schema.sql` is normalized and includes indexes for common searches.
- `database/backup-restore.ps1` demonstrates PostgreSQL backup and restore.
- `.github/workflows/ci.yml` runs tests and validates Compose on every push and pull request.

## Branch convention

Use `feature/<area>` branches, for example `feature/auth`, `feature/academic`, `feature/database`, and `feature/gateway`.
