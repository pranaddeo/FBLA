# First import need so we can acess the rest of our code
from website import create_app
# Starts app to run
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)