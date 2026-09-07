$ErrorActionPreference = "Stop"
$baseUrl = "http://localhost:8000"
$studentId = "STU-DEMO-001"
$adminEmail = "demo-$([Guid]::NewGuid().ToString('N').Substring(0, 8))@example.com"

function Invoke-Json {
    param(
        [string]$Method,
        [string]$Path,
        [object]$Body,
        [hashtable]$Headers = @{}
    )
    $request = @{ Method = $Method; Uri = "$baseUrl$Path"; Headers = $Headers }
    if ($null -ne $Body) {
        $request.ContentType = "application/json"
        $request.Body = $Body | ConvertTo-Json -Depth 10
    }
    return Invoke-RestMethod @request
}

$ready = $false
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    try {
        $health = Invoke-Json -Method Get -Path "/health"
        if ($health.status -eq "ok") {
            $ready = $true
            break
        }
    } catch {
        # The gateway may still be starting.
    }
}
if (-not $ready) {
    throw "Gateway did not become ready at $baseUrl"
}

$admin = Invoke-Json -Method Post -Path "/api/v1/auth/register" -Body @{
    name = "Demo Admin"
    email = $adminEmail
    password = "correct horse"
    role = "admin"
}
$login = Invoke-Json -Method Post -Path "/api/v1/auth/login" -Body @{
    email = $adminEmail
    password = "correct horse"
}
$headers = @{ Authorization = "Bearer $($login.access_token)" }
$me = Invoke-Json -Method Get -Path "/api/v1/auth/me" -Headers $headers
$transcript = Invoke-Json -Method Post -Path "/api/v1/academic/transcripts" -Body @{
    student_id = $studentId
    student_name = "Demo Student"
    grades = @(
        @{ course_code = "SEN4121"; course_name = "Large Systems"; score = 80; credit_units = 3 },
        @{ course_code = "SEN4122"; course_name = "Software Engineering"; score = 70; credit_units = 2 }
    )
}
$invoice = Invoke-Json -Method Post -Path "/api/v1/finance/invoices" -Body @{
    student_id = $studentId
    tuition = 1200
    accommodation = 300
    other_fees = 50
}
$payroll = Invoke-Json -Method Post -Path "/api/v1/hr/payroll" -Body @{
    employee_id = "EMP-DEMO-001"
    gross_salary = 5000
    pension_rate = 0.08
    tax_rate = 0.10
}
$enrollment = Invoke-Json -Method Post -Path "/api/v1/academic/enrollments" -Body @{
    student_id = $studentId
    tuition = 1200
    accommodation = 300
    other_fees = 50
}

$eventInvoice = $null
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    $eventInvoices = Invoke-Json -Method Get -Path "/api/v1/finance/invoices/$studentId"
    if ($eventInvoices.Count -gt 1) {
        $eventInvoice = $eventInvoices[-1]
        break
    }
}
if ($null -eq $eventInvoice) {
    throw "Enrollment event did not produce a Finance invoice"
}

$rateLimitStatuses = @()
for ($attempt = 0; $attempt -lt 11; $attempt++) {
    try {
        Invoke-Json -Method Get -Path "/api/v1/unknown" | Out-Null
        $rateLimitStatuses += 404
    } catch {
        $rateLimitStatuses += [int]$_.Exception.Response.StatusCode
    }
}
if ($rateLimitStatuses[-1] -ne 429) {
    throw "Rate limit was not triggered"
}

[ordered]@{
    gateway = "ok"
    authenticated_user = $me.email
    transcript_average = $transcript.average_score
    invoice_amount = $invoice.amount
    payroll_net = $payroll.net_salary
    enrollment = $enrollment.status
    async_invoice_amount = $eventInvoice.amount
    rate_limit_final_status = $rateLimitStatuses[-1]
} | ConvertTo-Json
