from sqlalchemy import select

from todo_list.models import User


def test_create_user(session):
    new_user = User(username='wagner', password='password', email='test@test.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'wagner'))
    assert user.username == 'wagner'
    assert user.id == 1
