# -*- coding: utf-8 -*-
from flask import Flask
import app.config as config

app = Flask(__name__)
app.config.from_object(config)
app.template_folder = "templates"

from app import routes