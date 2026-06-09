from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2.extras import execute_values
import csv
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session state


# Database Logic
# -----------------

def save_results_to_db(risk_percentage, answers):
    if not DATABASE_URL:
        print("DATABASE_URL is not configured. Skipping...")
        return
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        age_group = answers.get('1', {}).get('text', 'Nie podano')
        gender = answers.get('2', {}).get('text', 'Nie podano')
        education_profile = answers.get('3', {}).get('text', 'Nie podano')
        
        cur.execute(
            """
            INSERT INTO submissions (total_score, age_group, gender, education_profile) 
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (risk_percentage, age_group, gender, education_profile)
        )
        submission_id = cur.fetchone()[0]
        
        user_answers_data = []
        for q_id, data in answers.items():
            if int(q_id) > 3:
                user_answers_data.append((
                    submission_id,
                    int(q_id),
                    data['category'],
                    data['text'],
                    data['points']
                ))
            
        if user_answers_data:
            execute_values(
                cur,
                """
                INSERT INTO user_answers (submission_id, question_id, category, selected_option, points_earned) 
                VALUES %s
                """,
                user_answers_data
            )
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully saved submission with ID: {submission_id}")
    except Exception as e:
        print(f"Database write error: {e}")


# Flask App
# -----------------

def load_database():
    categories = []
    questions_by_category = {}
    
    with open('database.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cat = row['Category']
            if cat not in categories:
                categories.append(cat)
                questions_by_category[cat] = []
            
            # Parse pipe-separated values
            options = row['Options'].split('|')
            points = [int(p) for p in row['Points'].split('|')]
            
            questions_by_category[cat].append({
                'id': row['ID'],
                'question': row['Question'],
                'options': list(zip(options, points)),
                'weight': int(row['Weight'])
            })
            
    return categories, questions_by_category

@app.route('/')
def index():
    session.clear() # Reset survey on start
    return render_template('index.html')

@app.route('/section/<int:section_id>', methods=['GET', 'POST'])
def section(section_id):
    categories, questions_data = load_database()
    
    if section_id >= len(categories):
        answers = session.get('answers', {})
        
        numerator = sum(d.get('points', 0) * d.get('weight', 0) for d in answers.values())
        denominator = sum(10 * d.get('weight', 0) for d in answers.values())
        risk_percentage = round((numerator / denominator) * 100, 2) if denominator > 0 else 0
        
        save_results_to_db(risk_percentage, answers)

        return redirect(url_for('result'))
        
    current_category = categories[section_id]
    questions = questions_data[current_category]
    
    if request.method == 'POST':
        if 'answers' not in session:
            session['answers'] = {}
            
        answers = session['answers']
        for q in questions:
            q_id = str(q['id'])
            
            selected_idx_raw = request.form.get(f'q_{q_id}')
            
            if selected_idx_raw is not None:
                selected_idx = int(selected_idx_raw)
                
                option_text, option_points = q['options'][selected_idx]
                
                answers[q_id] = {
                    'category': current_category,
                    'text': option_text,
                    'points': option_points,
                    'weight': q['weight']
                }
            
        session['answers'] = answers 
        session.modified = True
        return redirect(url_for('section', section_id=section_id + 1))

    progress = f"{int((section_id / len(categories)) * 100)}%"
    return render_template('section.html', 
                           category=current_category, 
                           questions=questions, 
                           progress=progress,
                           section_id=section_id)

@app.route('/result')
def result():
    answers = session.get('answers', {})
    if not answers:
        return redirect(url_for('index'))
        
    numerator = 0
    denominator = 0
    
    # Calculate AMORO Score based on the formula
    for q_id, data in answers.items():
        p = data['points']
        w = data['weight']
        numerator += (p * w)
        denominator += (10 * w)
        
    risk_percentage = (numerator / denominator) * 100 if denominator > 0 else 0
    risk_percentage = round(risk_percentage, 2)
    
    # Determine risk level based on thresholds
    if risk_percentage <= 25:
        level, color, desc = "Minimalne", "success", "Wzorowa higiena cyfrowa. Bardzo trudny cel dla analityka OSINT."
    elif risk_percentage <= 50:
        level, color, desc = "Umiarkowane", "warning", "Przeciętny użytkownik. Istnieją luki pozwalające na podstawowe profilowanie."
    elif risk_percentage <= 75:
        level, color, desc = "Wysokie", "danger", "Poważne zagrożenie prywatności. Profil podatny na zautomatyzowane ataki."
    else:
        level, color, desc = "Krytyczne", "dark", "Otwarta księga. Życie cyfrowe osoby badanej jest w pełni transparentne."
        
    return render_template('result.html', score=risk_percentage, level=level, color=color, desc=desc)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)