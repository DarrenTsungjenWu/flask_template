from flask import Blueprint

blueprint = Blueprint(
    'dashboard',
    __name__,
    url_prefix="",
    template_folder = 'templates',
    static_folder = 'static'
)