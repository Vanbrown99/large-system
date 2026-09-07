# API Contract

All production requests enter through `http://localhost:8000`.

| Method | Gateway endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Gateway health |
| POST | `/api/v1/auth/register` | Register admin or student |
| POST | `/api/v1/auth/login` | Issue JWT |
| GET | `/api/v1/auth/me` | Inspect authenticated user |
| GET | `/api/v1/auth/admin/overview` | Admin-only route |
| POST | `/api/v1/academic/transcripts` | Generate weighted transcript |
| POST | `/api/v1/finance/invoices` | Generate fee invoice |
| POST | `/api/v1/hr/payroll` | Calculate payroll deductions |

Interactive OpenAPI documentation is generated at `/docs` by FastAPI.
