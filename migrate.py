from re import findall
from subprocess import run


def main() -> None:
    """
    Create revision with autogenerate

    :return:
    """
    try:
        version = int(input("* input this version : v"))
    except (ValueError, TypeError):
        print("* FAILED : version must be int")
        return

    output = run(
        f"alembic revision --autogenerate -m v{version}",
        capture_output=True,
        check=False
    )

    print()
    for error in output.stderr.split(b"\n"):
        print(error.decode().strip())

    print(output.stdout.decode())

    if output.stdout.startswith(b"Generating"):
        revision = findall(
            pattern="([A-z0-9]{12})_v[0-9].py",
            string=output.stdout.decode()
        )[0]

        run(
            f"alembic upgrade {revision}",
            check=False
        )


if __name__ == "__main__":
    main()
