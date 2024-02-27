from flask import Flask

app = Flask(__name__)

USERS = list()
CONTESTS = list()

from app import views
from app import models
