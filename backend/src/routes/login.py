from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('login', __name__)
