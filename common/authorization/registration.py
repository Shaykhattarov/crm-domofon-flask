from app import db
from app.models import User


def create_user(name: str, email: str, address: str, phone: str, role_id: int = 1) -> bool:
    user = User(
        name=name, 
        email=email,
        address=address,
        phone=phone,
        role_id=role_id
    )
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        return False
    
    return True
