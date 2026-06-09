-- migrate:up

-- submissions table constraints
ALTER TABLE submissions 
    ADD CONSTRAINT check_total_score 
    CHECK (total_score >= 0.00 AND total_score <= 100.00);

ALTER TABLE submissions 
    ADD CONSTRAINT check_age_group_not_empty 
    CHECK (length(trim(age_group)) > 0);

ALTER TABLE submissions 
    ADD CONSTRAINT check_gender_not_empty 
    CHECK (length(trim(gender)) > 0);

ALTER TABLE submissions 
    ADD CONSTRAINT check_education_profile_not_empty 
    CHECK (length(trim(education_profile)) > 0);

-- user_answers table constraints
ALTER TABLE user_answers 
    ADD CONSTRAINT check_question_id_positive 
    CHECK (question_id > 0);

ALTER TABLE user_answers 
    ADD CONSTRAINT check_points_earned_non_negative 
    CHECK (points_earned >= 0);

ALTER TABLE user_answers 
    ADD CONSTRAINT check_selected_option_not_empty 
    CHECK (length(trim(selected_option)) > 0);

ALTER TABLE user_answers 
    ADD CONSTRAINT check_category_not_empty 
    CHECK (length(trim(category)) > 0);


-- migrate:down

ALTER TABLE user_answers DROP CONSTRAINT IF EXISTS check_category_not_empty;
ALTER TABLE user_answers DROP CONSTRAINT IF EXISTS check_selected_option_not_empty;
ALTER TABLE user_answers DROP CONSTRAINT IF EXISTS check_points_earned_non_negative;
ALTER TABLE user_answers DROP CONSTRAINT IF EXISTS check_question_id_positive;

ALTER TABLE submissions DROP CONSTRAINT IF EXISTS check_education_profile_not_empty;
ALTER TABLE submissions DROP CONSTRAINT IF EXISTS check_gender_not_empty;
ALTER TABLE submissions DROP CONSTRAINT IF EXISTS check_age_group_not_empty;
ALTER TABLE submissions DROP CONSTRAINT IF EXISTS check_total_score;