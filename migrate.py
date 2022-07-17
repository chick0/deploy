from re import findall
from subprocess import run


def main():
    try:
        version = int(input("* input this version : v"))
    except (ValueError, TypeError):
        print("* FAILED : version must be int")
        return -1

    output = run(
        f"alembic revision --autogenerate -m v{version}",
        capture_output=True
    )

    print()
    for p in output.stderr.split(b"\n"):
        print(p.decode().strip())

    print(output.stdout.decode())

    if output.stdout.startswith(b"Generating"):
        revision = findall(
            pattern="([A-z0-9]{12})_v[0-9].py",
            string=output.stdout.decode()
        )[0]

        run(f"alembic upgrade {revision}")


if __name__ == "__main__":
    main()
