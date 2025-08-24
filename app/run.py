from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    # TODO: Dodać do testów sprawdzanie, czy przy usuwaniu jest wywoływane repo
