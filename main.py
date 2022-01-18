# -*- coding: utf-8 -*-
"""The main module for launching Heroku application"""

from os import environ
from app.routes import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
