import peewee
import uuid
import pathlib


class Database:

    def __init__(self, name):
        ''' Define a database class and assing a name for it'''
        self.name = name

    def create_database(self):
        ''' Create the database make path models in it and connect to it'''
        self.db = peewee.SqliteDatabase(self.name)

        global Path

        class Path(peewee.Model):
            id = peewee.IntegerField()
            path = peewee.TextField()

            class Meta:
                database = self.db
        self.db.connect()
        self.db.create_tables([Path])

    def make_new_image(telegram_id):
        '''Makes new row in our database and takes care of new path'''
        new_img_name = uuid.uuid4()
        folder_path = pathlib.Path('./Photo')
        if(pathlib.Path.is_dir(folder_path) == False):
            pathlib.Path.mkdir(folder_path)
        pathlib.Path.mkdir(folder_path/f'{new_img_name}')
        path = pathlib.Path(folder_path/f'{new_img_name}/{new_img_name}.jpg')
        new_obj = Path.create(id=telegram_id, path=path)
        return path

    def fetch_image(telegram_id):
        '''Fetch image path from db'''
        image_path = Path.select().where(Path.id == telegram_id).get().path
        return image_path
