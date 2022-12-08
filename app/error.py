from flask import redirect


class RedirectRequired(Exception):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path


def handle_redirect_required(error: RedirectRequired):
    return redirect(error.path)
