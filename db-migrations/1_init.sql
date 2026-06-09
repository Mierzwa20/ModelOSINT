-- migrate:up

SET TIME ZONE 'UTC';

-- table for storing submissions summary and demographic data
CREATE TABLE IF NOT EXISTS submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    completed_at TIMESTAMPTZ DEFAULT now(),
    total_score NUMERIC(5, 2) NOT NULL,
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    education_profile TEXT NOT NULL
);

-- table for storing individual case results
CREATE TABLE IF NOT EXISTS user_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(id) ON DELETE CASCADE,
    question_id INT NOT NULL,
    category TEXT NOT NULL,
    selected_option TEXT NOT NULL,
    points_earned INT NOT NULL
);


-- migrate:down

DROP TABLE IF EXISTS user_answers;
DROP TABLE IF EXISTS submissions;