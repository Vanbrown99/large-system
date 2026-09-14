# School ERP Software Requirements Specification

## Scope

The School ERP coordinates authentication, academic records, finance, and HR operations through independently deployable services.

## Functional requirements

- Users can register and log in as administrators or students.
- Authenticated users can generate academic transcripts, enroll students, create and retrieve finance invoices, and calculate HR payroll through the gateway.
- Services expose health endpoints and OpenAPI documentation.
- An enrollment publishes a `StudentEnrolled` RabbitMQ event and Finance creates an invoice asynchronously.

## Non-functional requirements

- Passwords must be bcrypt-hashed.
- JWTs must expire and be signed with a secret stored outside source control.
- Requests must enter through the gateway and be rate limited.
- MySQL stores users, transcripts with grades, enrollments, invoices, and payroll records. The tables are normalized, indexed, and restorable from backup.
- Automated tests must run in CI on every push and pull request.

## Roles

- Admin: authenticated platform operator with privileged administrative actions.
- Student: authenticated user who can access student-facing operations.
