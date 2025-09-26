#!/usr/bin/env python3

from random import randint
from faker import Faker

from app import app
from models import db, Article, User  # make sure your models.py exports db

fake = Faker()

# Ensure app context is active
with app.app_context():
    print("Deleting all records...")
    Article.query.delete()
    User.query.delete()
    db.session.commit()  # commit deletions

    print("Creating users...")
    users = []
    usernames = []
    for _ in range(25):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)
        users.append(User(username=username))

    db.session.add_all(users)

    print("Creating articles...")
    articles = []
    for _ in range(100):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + "..."
        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
        )
        articles.append(article)

    db.session.add_all(articles)
    db.session.commit()  # commit all new data

    print("Complete.")
