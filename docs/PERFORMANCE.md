# Load Test Evidence

The performance check sends 10 virtual users to the public gateway health endpoint for 30 seconds. It records request timing and requires the 95th percentile response time to be below 500 ms with fewer than 1% failed requests.

From the project root, run:

```powershell
docker run --rm --network large_sytem_default -e BASE_URL=http://gateway:8000 -v "${PWD}/docs:/scripts" grafana/k6 run /scripts/load-test.js
```

Record the resulting `http_req_duration` and `http_req_failed` values below during the examiner demonstration.

| Date | p(95) duration | Failed requests | Result |
| --- | --- | --- | --- |
| 2026-09-14 | 34.14 ms | 0.00% (0 of 300) | Pass |