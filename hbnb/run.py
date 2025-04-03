from hbnb.app import create_app, db

app = create_app()

@app.cli.command("create_database")
def create_database():
    """Crea todas las tablas en la base de datos."""
    try:
        db.create_all()
        print("Base de datos creada correctamente.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

if __name__ == '__main__':
    app.run(debug=True)