from sql import get_session
from sql.models import User
from sql.models import Project


def main() -> None:
    """
    Delete user with user email

    :return:
    """
    session = get_session()

    email = input("email=")

    user: User = session.query(User).filter_by(
        email=email
    ).first()

    if user is None:
        print("-> undefined user")
        return

    project: int = session.query(Project).filter_by(
        owner=user.uuid
    ).count()

    if project != 0:
        print(f"-> this user has {project} project.")
        print("-> request ignored")
        return

    print()
    print("*", user.uuid)
    print("*", user.email)
    if input("* delete this user? (y/n)").lower() == "y":
        session.delete(user)
        session.commit()

        print()
        print("-> user deleted")
    else:
        print()
        print("-> request ignored")

    session.close()


if __name__ == "__main__":
    main()
