import database
import models
import random
import datetime

def populate():
    # Make sure tables are created
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    if db.query(models.User).filter(models.User.email == "alice@mock.com").first():
        print("Mock data already exists.")
        db.close()
        return

    users_data = [
        {"email": "alice@mock.com", "name": "Alice Smith", "role": "user", "is_active": 1},
        {"email": "bob@mock.com", "name": "Bob Jones", "role": "user", "is_active": 1},
        {"email": "carol@mock.com", "name": "Carol White", "role": "user", "is_active": 0},
        {"email": "dave@mock.com", "name": "Dave Brown", "role": "user", "is_active": 1},
    ]
    
    new_users = []
    for ud in users_data:
        u = models.User(**ud)
        db.add(u)
        new_users.append(u)
        
    db.commit()
    
    for u in new_users:
        db.refresh(u)
        num_msgs = random.randint(15, 45)
        for _ in range(num_msgs):
            msg_type = random.choice(["sms", "email"])
            prediction = random.choice(["Safe", "Spam", "Safe", "Safe"])
            confidence = random.uniform(0.55, 0.99)
            
            m = models.Message(
                content=f"Mock {msg_type} message content...",
                msg_type=msg_type,
                prediction=prediction,
                confidence=confidence,
                user_id=u.id,
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0, 30), hours=random.randint(0, 24))
            )
            db.add(m)
            
    db.commit()
    db.close()
    print("Successfully populated standard mock users and scan activity.")

if __name__ == "__main__":
    populate()
