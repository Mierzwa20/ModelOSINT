from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session state

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
        return redirect(url_for('result'))
        
    current_category = categories[section_id]
    questions = questions_data[current_category]
    
    if request.method == 'POST':
        if 'answers' not in session:
            session['answers'] = {}
            
        answers = session['answers']
        for q in questions:
            q_id = str(q['id'])
            # Save the selected points and the weight for final calculation
            selected_points = int(request.form.get(f'q_{q_id}'))
            answers[q_id] = {'points': selected_points, 'weight': q['weight']}
            
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