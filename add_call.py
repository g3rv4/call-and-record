import argparse
from dateutil.parser import parse as parse_date
import pytz
from models import ScheduledCall

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="call name", required=True)
parser.add_argument("--start-at", help="time to start", required=True)
parser.add_argument("--end-at", help="time to end", required=True)
parser.add_argument("--phone-number", help="phone number", required=True)
parser.add_argument("--dtmf", help="DTMF to send on connection", required=True)
parser.add_argument("--timezone", help="timezone in pytz format, defaults to eastern", default='US/Eastern')
args = parser.parse_args()

try:
    tz = pytz.timezone(args.timezone)

    # parse the dates
    start_at = parse_date(args.start_at)
    end_at = parse_date(args.end_at)

    # localize them
    start_at = tz.localize(start_at)
    end_at = tz.localize(end_at)

    # convert to UTC and remove timezone info
    start_at = start_at.astimezone(pytz.utc).replace(tzinfo=None)
    end_at = end_at.astimezone(pytz.utc).replace(tzinfo=None)

    # the amount of seconds can't be greater than 99999
    if (end_at - start_at).total_seconds() > 99999:
        print 'The call is too long, it can not exceed 99999 seconds\n'
        exit(1)
except:
    parser.print_help()
    exit(1)

call = ScheduledCall(name=args.name, phone_number=args.phone_number, dtmf=args.dtmf, start_at_utc=start_at, end_at_utc=end_at, timezone=args.timezone)
call.save()
