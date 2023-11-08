# Import the create_app function from the "website" module
from website import create_app

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Create a Flask application using the create_app function
    app = create_app()

    # Run the Flask application in debug mode, allowing for detailed error messages and automatic code reloading
    app.run(debug=True)
