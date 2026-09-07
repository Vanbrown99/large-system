CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'student')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE students (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    student_number VARCHAR(30) NOT NULL UNIQUE,
    programme VARCHAR(120) NOT NULL
);

CREATE TABLE courses (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    credit_units INTEGER NOT NULL CHECK (credit_units > 0)
);

CREATE TABLE grades (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES students(id),
    course_id BIGINT NOT NULL REFERENCES courses(id),
    score NUMERIC(5,2) NOT NULL CHECK (score BETWEEN 0 AND 100),
    UNIQUE (student_id, course_id)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_students_programme ON students(programme);
