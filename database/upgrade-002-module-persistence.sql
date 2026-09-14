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