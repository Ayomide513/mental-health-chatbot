import re
import numpy as np

def extract_number(text, min_val=0, max_val=100):
    numbers = re.findall(r'\d+\.?\d*', text)
    if numbers:
        num = float(numbers[0])
        return max(min_val, min(num, max_val))
    return None

def get_risk_level(probability):
    if probability < 30:
        return "Low", "green"
    elif probability < 60:
        return "Moderate", "orange"
    else:
        return "High", "red"

def encode_department(department):
    return {
        'business': 1 if department.lower() == "business" else 0,
        'engineering': 1 if department.lower() == "engineering" else 0,
        'medical': 1 if department.lower() == "medical" else 0,
        'science': 1 if department.lower() == "science" else 0
    }

def encode_gender(gender):
    return 1 if gender.lower() == "male" else 0

def prepare_input(data):
    dept = encode_department(data['department'])
    
    return np.array([[
        data['age'],
        encode_gender(data['gender']),
        data['cgpa'],
        data['sleep'],
        data['study'],
        data['social_media'],
        data['exercise'],
        data['stress'],
        dept['business'],
        dept['engineering'],
        dept['medical'],
        dept['science']
    ]])

def generate_recommendations(data):
    recommendations = []
    
    if data['sleep'] < 7:
        recommendations.append({
            "area": "Sleep",
            "issue": f"Sleeping {data['sleep']} hours/night",
            "action": "Aim for 7-9 hours. Set consistent bedtime."
        })
    
    if data['stress'] >= 7:
        recommendations.append({
            "area": "Stress",
            "issue": f"Stress level: {data['stress']}/10",
            "action": "Try meditation or talk to a counselor."
        })
    
    if data['exercise'] < 150:
        recommendations.append({
            "area": "Exercise",
            "issue": f"{data['exercise']} min/week",
            "action": "Aim for 150 min/week. Start with 30-min walks."
        })
    
    if data['social_media'] > 5:
        recommendations.append({
            "area": "Social Media",
            "issue": f"{data['social_media']} hours/day",
            "action": "Reduce to 2-3 hours. Use app timers."
        })
    
    if data['cgpa'] < 2.5:
        recommendations.append({
            "area": "Academics",
            "issue": f"CGPA: {data['cgpa']}",
            "action": "Talk to advisor, consider tutoring."
        })
    
    return recommendations