from flask_app import app

# remember to import your controllers
from flask_app.controllers import habit_controller
from flask_app.controllers import user_controller

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)