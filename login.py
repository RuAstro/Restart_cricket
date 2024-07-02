from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required,
)
from sqlalchemy.orm import relationship


# Initialize Flask application
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SECRET_KEY"] = "JamesBondSecretKey"
app.config["SECURITY_REGISTERABLE"] = True

# Initialize Flask extensions
db = SQLAlchemy(app)
Bootstrap(app)
mail = Mail(app)

# Define association table for many-to-many relationship
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


# Define Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create database tables before the first request is handled
@app.before_first_request
def setup_database():
    db.create_all()


# Route for rendering index template
@app.route("/")
@login_required  # Example of protecting a route with login_required decorator
def index():
    return render_template("index.html")


# Run the application
if __name__ == "__main__":
    app.run()
