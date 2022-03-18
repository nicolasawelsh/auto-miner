# Imported libraries
import pickle

# Local libraries
from config.dicts import alerts, dbfile


def write_db(db=alerts):
    with open(dbfile, 'wb') as handle:
        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)


def build_db():
    write_db(db=alerts)


def read_db():
    try:
        with open(dbfile, 'rb') as handle:
            db = pickle.load(handle)
    except FileNotFoundError:
        build_db()
        db = read_db()
    return db


if __name__ == "__main__":
    build_db()
