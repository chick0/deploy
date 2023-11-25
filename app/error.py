from flask import render_template


def handle_404(e):
    return render_template(
        "error/404.jinja2"
    ), 404
