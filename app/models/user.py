from datetime import datetime

class User:
    """User model for Firestore"""
    
    def __init__(self, uid, email, name, role='customer', created_at=None):
        self.uid = uid
        self.email = email
        self.name = name
        self.role = role  # 'customer' or 'staff'
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get('uid'),
            email=data.get('email'),
            name=data.get('name'),
            role=data.get('role', 'customer'),
            created_at=data.get('created_at')
        )