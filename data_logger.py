import pandas as pd
import os
from datetime import datetime

class DataLogger:
    def __init__(self, filepath='user_assessments.csv'):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            df = pd.DataFrame(columns=[
                'timestamp', 'age', 'gender', 'cgpa', 'sleep_duration',
                'study_hours', 'social_media_hours', 'physical_activity',
                'stress_level', 'department', 'predicted_risk', 
                'predicted_label', 'risk_level'
            ])
            df.to_csv(self.filepath, index=False)
    
    def log_assessment(self, user_data, prediction, probability, risk_level):
        new_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'age': user_data['age'],
            'gender': user_data['gender'],
            'cgpa': user_data['cgpa'],
            'sleep_duration': user_data['sleep'],
            'study_hours': user_data['study'],
            'social_media_hours': user_data['social_media'],
            'physical_activity': user_data['exercise'],
            'stress_level': user_data['stress'],
            'department': user_data['department'],
            'predicted_risk': round(probability, 2),
            'predicted_label': int(prediction),
            'risk_level': risk_level
        }
        
        df = pd.read_csv(self.filepath)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.filepath, index=False)
        
        return True
    
    def get_stats(self):
        if os.path.exists(self.filepath):
            df = pd.read_csv(self.filepath)
            if len(df) > 0:
                return {
                    'total_assessments': len(df),
                    'high_risk_count': len(df[df['risk_level'] == 'High']),
                    'average_risk': df['predicted_risk'].mean(),
                    'latest_assessment': df['timestamp'].iloc[-1] if len(df) > 0 else None
                }
        return None