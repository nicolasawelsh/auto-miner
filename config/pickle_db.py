import pickle


dbfile = 'dbfile'

alerts = {
    'repair_needed'    : False,
    'monster_appeared' : False
}


def write_db(db=alerts):
    with open(dbfile, 'wb') as handle:
        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)


def build_db():
    write_db(db=alerts)


def read_db():
    with open(dbfile, 'rb') as handle:
        db = pickle.load(handle)
    return db


if __name__ == "__main__":
    build_db()
    