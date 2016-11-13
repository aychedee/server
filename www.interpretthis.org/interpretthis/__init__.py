# interpretthis.org, requires this done to use the decorators in views
from flask import Flask
app = Flask(__name__)

from interpretthis import views
