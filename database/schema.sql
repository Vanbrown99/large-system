CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_users_role CHECK (role IN ('admin', 'student'))
);

CREATE TABLE IF NOT EXISTS students (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    student_number VARCHAR(30) NOT NULL UNIQUE,
    programme VARCHAR(120) NOT NULL,
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS courses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    credit_units INT NOT NULL,
    CONSTRAINT chk_courses_credits CHECK (credit_units > 0)
);

CREATE TABLE IF NOT EXISTS grades (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    UNIQUE KEY uq_grades_student_course (student_id, course_id),
    CONSTRAINT fk_grades_student FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_grades_course FOREIGN KEY (course_id) REFERENCES courses(id),
    CONSTRAINT chk_grades_score CHECK (score BETWEEN 0 AND 100)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_students_programme ON students(programme);

CREATE TABLE IF NOT EXISTS academic_transcripts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    average_score DECIMAL(5,2) NOT NULL,
    credits INT NOT NULL,
    standing VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transcripts_student_id (student_id)
);

CREATE TABLE IF NOT EXISTS academic_transcript_grades (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transcript_id BIGINT NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    course_name VARCHAR(150) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    credit_units INT NOT NULL,
    CONSTRAINT fk_transcript_grades_transcript FOREIGN KEY (transcript_id) REFERENCES academic_transcripts(id),
    CONSTRAINT chk_transcript_grades_score CHECK (score BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS academic_enrollments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    tuition DECIMAL(10,2) NOT NULL,
    accommodation DECIMAL(10,2) NOT NULL DEFAULT 0,
    other_fees DECIMAL(10,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_enrollments_student_id (student_id)
);

CREATE TABLE IF NOT EXISTS finance_invoices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_invoices_student_id (student_id)
);

CREATE TABLE IF NOT EXISTS hr_payroll (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    gross_salary DECIMAL(10,2) NOT NULL,
    pension DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2) NOT NULL,
    net_salary DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payroll_employee_id (employee_id)
);
