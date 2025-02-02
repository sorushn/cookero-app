from backend.app.core.db import get_session

def test_connectivity(settings):
    with get_session() as session:
        session.run("RETURN 1")

def test_create_user(session):
    session.run("CREATE (u:User {name: $name}) RETURN u", name="testuser")

def test_delete_user(session):
    session.run("CREATE (u:User {name: $name}) RETURN u", name="testuser")
    session.run("MATCH (u:User {name: $name}) DELETE u", name="testuser")

def  test_list_users(session):
    session.run("CREATE (u:User {name: $name}) RETURN u", name="testuser1")
    session.run("CREATE (u:User {name: $name}) RETURN u", name="testuser2")
    users = session.run("MATCH (u:User) RETURN u")
    assert len(users.data()) == 2

def test_create_recipe(session):
    session.run("CREATE (r:Recipe {name: $name}) RETURN r", name="testrecipe")
    session.run("MATCH (r:Recipe {name: $name}) DELETE r", name="testrecipe")
