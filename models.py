from peewee import *
import pytz
import os
from settings import settings

db = SqliteDatabase(os.path.join(settings['sqlite_path'], 'call_and_record.db'))


class ScheduledCall(Model):
    name = CharField()
    start_at_utc = DateTimeField()
    end_at_utc = DateTimeField()
    timezone = CharField()
    phone_number = CharField()
    dtmf = CharField()
    started = BooleanField(default=False)

    @property
    def start_at(self):
        return pytz.utc.localize(self.start_at_utc).astimezone(pytz.timezone(self.timezone))

    @property
    def end_at(self):
        return pytz.utc.localize(self.end_at_utc).astimezone(pytz.timezone(self.timezone))

    class Meta:
        database = db