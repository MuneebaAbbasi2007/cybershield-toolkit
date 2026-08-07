from zxcvbn import zxcvbn

def check_password_strength(password):
    result = zxcvbn(password)
    
    score = result['score']  # 0 (weak) to 4 (strong)
    feedback = result['feedback']
    
    strength_labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }
    
    return {
        "score": score,
        "strength": strength_labels[score],
        "warning": feedback.get('warning', ''),
        "suggestions": feedback.get('suggestions', [])
    }
    