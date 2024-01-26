from factory import create_app
from models import db

app = create_app('config.Config')


@app.cli.command('create_database')
def create_database():
    db.create_all()


@app.cli.command('drop_database')
def drop_database():
    db.drop_all()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
