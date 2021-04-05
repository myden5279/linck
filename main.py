from website import create_app

App = create_app()  # this is a objects of the Flask class

if __name__ == "__main__":
    App.run(debug=True)
