const output = document.querySelector('#output');
const responseTitle = document.querySelector('#responseTitle');
let token = '';

function show(title, data) {
  responseTitle.textContent = title;
  output.textContent = JSON.stringify(data, null, 2);
}

async function request(path, method, data, authenticated = false) {
  const response = await fetch(`/api/v1${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...(authenticated && token ? { Authorization: `Bearer ${token}` } : {}) },
    body: data ? JSON.stringify(data) : undefined,
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail || `Request failed (${response.status})`);
  return result;
}

function values(form) {
  return Object.fromEntries(new FormData(form));
}

function numeric(data, keys) {
  keys.forEach((key) => { data[key] = Number(data[key]); });
  return data;
}

function attach(id, path, transform, title, authenticated = false) {
  document.querySelector(id).addEventListener('submit', async (event) => {
    event.preventDefault();
    try { show('Request in progress', { endpoint: path }); show(title, await request(path, 'POST', transform(values(event.currentTarget)), authenticated)); }
    catch (error) { show('Request failed', { error: error.message }); }
  });
}

attach('#registerForm', '/auth/register', values, 'User registered');
document.querySelector('#loginForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  try { const result = await request('/auth/login', 'POST', values(event.currentTarget)); token = result.access_token; show('Access token issued', { token_type: result.token_type, authenticated: true }); }
  catch (error) { show('Sign-in failed', { error: error.message }); }
});
document.querySelector('#profileButton').addEventListener('click', async () => {
  try { show('Current user', await request('/auth/me', 'GET', null, true)); } catch (error) { show('Profile unavailable', { error: error.message }); }
});
attach('#transcriptForm', '/academic/transcripts', (data) => ({ student_id: data.student_id, student_name: data.student_name, grades: [{ course_code: 'MTH101', course_name: 'Mathematics', score: Number(data.math_score), credit_units: 3 }, { course_code: 'CSC101', course_name: 'Computer Science', score: Number(data.cs_score), credit_units: 3 }] }), 'Transcript generated');
attach('#enrollmentForm', '/academic/enrollments', (data) => numeric(data, ['tuition', 'accommodation', 'other_fees']), 'Enrollment published');
attach('#invoiceForm', '/finance/invoices', (data) => numeric(data, ['tuition', 'accommodation', 'other_fees']), 'Invoice created');
document.querySelector('#invoiceListForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  try { const id = values(event.currentTarget).student_id; show('Student invoices', await request(`/finance/invoices/${encodeURIComponent(id)}`, 'GET')); } catch (error) { show('Invoice lookup failed', { error: error.message }); }
});
attach('#payrollForm', '/hr/payroll', (data) => numeric(data, ['gross_salary', 'pension_rate', 'tax_rate']), 'Payroll calculated');
document.querySelectorAll('.tab').forEach((tab) => tab.addEventListener('click', () => {
  document.querySelectorAll('.tab, .panel').forEach((item) => item.classList.remove('active'));
  tab.classList.add('active'); document.querySelector(`#${tab.dataset.panel}`).classList.add('active');
}));
fetch('/health').then((response) => response.json()).then(() => { document.querySelector('#gatewayStatus').textContent = 'Online'; }).catch(() => { document.querySelector('#gatewayStatus').textContent = 'Offline'; });