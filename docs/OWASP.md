# OWASP Top 10 Controls

| Risk | Control in this project |
| --- | --- |
| Broken access control | JWT validation and explicit admin role checks protect privileged routes. |
| Cryptographic failures | Passwords are bcrypt hashes; JWT secret is configured through environment variables. |
| Injection | Request validation uses Pydantic constraints; database work must use parameterized queries. |
| Security misconfiguration | Services run in containers, expose only the gateway publicly, and keep secrets out of source control. |
| Identification failures | Login returns the same generic error for unknown users and wrong passwords; rate limiting reduces brute force pressure. |
| Vulnerable components | CI installs pinned dependencies and runs on every push and pull request. |
