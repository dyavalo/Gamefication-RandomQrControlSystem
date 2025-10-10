from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Add sample users
    users = [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
    ]
    
    for user_data in users:
        if not User.query.filter_by(username=user_data['username']).first():
            hashed_password = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
            new_user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=hashed_password
            )
            db.session.add(new_user)
    db.session.commit()
    print("Users added to the database.")