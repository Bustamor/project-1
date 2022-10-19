# __init__.py
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "dasl32qrkqjrq34irj43lqjfqwelqjewrq3l;krj2q23sadkfjwe3"
