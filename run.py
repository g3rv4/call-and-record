import pytz
import datetime
import os
from settings import settings
from models import ScheduledCall
from boto.ses import SESConnection

now = datetime.datetime.now(pytz.utc).replace(tzinfo=None)

calls_to_start = list(ScheduledCall.select().where((ScheduledCall.started == False) & (ScheduledCall.start_at_utc <= now)))

if len(calls_to_start):
    for call in calls_to_start:
        seconds = (call.end_at_utc - now).total_seconds()
        if seconds > 0:
            seconds = ('%i' % seconds).zfill(5)
            content =  "Channel: SIP/0prime1%s@anveo\n" % call.phone_number
            content += "Callerid: +18185144510\n"
            content += "Context: supercontext\n"
            content += "Extension: _%s_%s\n" % (seconds, call.dtmf)
            content += "Priority: 2\n"
            with open(os.path.join(settings['asterisk']['call_file_path'], 'call%i.call' % call.id), 'w') as f:
                f.write(content)

        call.started = True
        call.save()

    connection = SESConnection(aws_access_key_id=settings['email']['aws']['access_key_id'],
                               aws_secret_access_key=settings['email']['aws']['secret_access_key'])

    subject = 'Starting calls'
    lines = ['Name: %s\nStart at: %s (%s)\nEnd at: %s\n\n-------' % (c.name, c.start_at, c.timezone, c.end_at) for c in calls_to_start]

    connection.send_email(settings['email']['from'], subject, '\n'.join(lines), settings['email']['to'], format='text')
