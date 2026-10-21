from uuid import uuid4


def unique_user():
    return {
        "email": f"qa.diplom.{uuid4().hex}@example.com",
        "password": f"P@ssword-{uuid4().hex[:12]}",
        "name": f"QA-{uuid4().hex[:8]}",
    }
