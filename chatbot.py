import streamlit as st
from utils import extract_number
from config import QUESTIONS, DEPARTMENTS

class MentalHealthChatbot:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.step = 0
        self.data = {}
        self.conversation_history = []
    
    def get_current_question(self):
        questions_order = ['age', 'gender', 'cgpa', 'sleep', 'study', 
                          'social_media', 'exercise', 'stress', 'department']
        
        if self.step < len(questions_order):
            return QUESTIONS[questions_order[self.step]]
        return None
    
    def process_response(self, user_input):
        questions_order = ['age', 'gender', 'cgpa', 'sleep', 'study', 
                          'social_media', 'exercise', 'stress', 'department']
        
        current_field = questions_order[self.step]
        
        self.conversation_history.append({
            "question": self.get_current_question(),
            "response": user_input
        })
        
        if current_field == 'age':
            value = extract_number(user_input, 16, 40)
            if value:
                self.data['age'] = int(value)
                self.step += 1
                return True, f"Got it! Age: {int(value)}"
            return False, "Please enter a valid age (16-40)"
        
        elif current_field == 'gender':
            if 'male' in user_input.lower():
                self.data['gender'] = 'Male' if 'female' not in user_input.lower() else 'Female'
                self.step += 1
                return True, f"Thanks! Gender: {self.data['gender']}"
            return False, "Please specify Male or Female"
        
        elif current_field == 'cgpa':
            value = extract_number(user_input, 0, 4)
            if value is not None:
                self.data['cgpa'] = round(value, 1)
                self.step += 1
                return True, f"Noted! CGPA: {self.data['cgpa']}"
            return False, "Please enter a CGPA between 0.0 and 4.0"
        
        elif current_field == 'sleep':
            value = extract_number(user_input, 0, 12)
            if value:
                self.data['sleep'] = value
                self.step += 1
                return True, f"Got it! Sleep: {value} hours/night"
            return False, "Please enter hours of sleep (0-12)"
        
        elif current_field == 'study':
            value = extract_number(user_input, 0, 16)
            if value:
                self.data['study'] = value
                self.step += 1
                return True, f"Understood! Study: {value} hours/day"
            return False, "Please enter study hours (0-16)"
        
        elif current_field == 'social_media':
            value = extract_number(user_input, 0, 16)
            if value:
                self.data['social_media'] = value
                self.step += 1
                return True, f"Got it! Social media: {value} hours/day"
            return False, "Please enter social media hours (0-16)"
        
        elif current_field == 'exercise':
            value = extract_number(user_input, 0, 500)
            if value:
                self.data['exercise'] = int(value)
                self.step += 1
                return True, f"Great! Exercise: {int(value)} min/week"
            return False, "Please enter exercise minutes per week (0-500)"
        
        elif current_field == 'stress':
            value = extract_number(user_input, 0, 10)
            if value is not None:
                self.data['stress'] = int(value)
                self.step += 1
                return True, f"Noted! Stress level: {int(value)}/10"
            return False, "Please enter stress level (0-10)"
        
        elif current_field == 'department':
            for dept in DEPARTMENTS:
                if dept.lower() in user_input.lower():
                    self.data['department'] = dept
                    self.step += 1
                    return True, f"Perfect! Department: {dept}"
            return False, f"Please specify: {', '.join(DEPARTMENTS)}"
        
        return False, "I didn't understand that. Can you try again?"
    
    def is_complete(self):
        return self.step >= 9
    
    def get_collected_data(self):
        return self.data