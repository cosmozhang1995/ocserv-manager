#!/usr/bin/env python

import sys, os
from logutil import search_log, add_log, timefmt
from utils import format_bytes, format_seconds
from configs import price_per_gb
import datetime

username = sys.argv[1]

# lastrecord = search_log(judgement=(lambda item: item.title in ["BillCalc", "Disconnect"])).first()
# if lastrecord and lastrecord.title == "BillCalc":
#   bytesin = int(lastrecord.params.get(bytesin))
#   bytesout = int(lastrecord.params.get(bytesout))
#   duration = int(lastrecord.params.get(duration))
#   hasrecord = True
# else:

lastpay = search_log(title="BillPay", user=username, limit=1).first()
starttime = lastpay.params.get("endtime") if lastpay else None
starthash = lastpay.params.get("endhash") if lastpay else None

bytesin = 0
bytesout = 0
duration = 0
records = search_log(title="Disconnect", user=username, start=starttime)
for record in records:
  if starthash and record.hashstr.find(starthash) == 0: break
  bytesin += int(record.params.get("bytesin"))
  bytesout += int(record.params.get("bytesout"))
  duration += int(record.params.get("duration"))
hasrecord = (len(records) > 0)

if hasrecord:
  totalprice = float(bytesin + bytesout) / 1000 / 1000 / 1000 * price_per_gb
  starttime = records[-1].time
  starthash = records[-1].hashstr
  endtime = records[0].time
  endhash = records[0].hashstr
  log = add_log(title="BillCalc", params=[
      ("user",username),
      ("starttime",starttime.strftime(timefmt)),
      ("starthash",starthash),
      ("endtime",endtime.strftime(timefmt)),
      ("endhash",endhash),
      ("bytesin",bytesin),
      ("bytesout",bytesout),
      ("duration",duration),
      ("totalprice",totalprice)
    ])

if hasrecord:
  print("Usage for user [%s]:" % username)
  print("  From <%s> to <%s>" % (starttime.strftime("%Y-%m-%d %H:%M:%S"), endtime.strftime("%Y-%m-%d %H:%M:%S")))
  print("    Total upload: " + format_bytes(bytesin))
  print("    Total download: " + format_bytes(bytesout))
  print("    Total usage: " + format_seconds(duration))
  print("    Total price: " + str(totalprice))
  print("  Hash code: " + log.hashstr)
else:
  print("No usage for user [%s] since <%s>" % (username, datetime.datetime.strptime(starttime,timefmt).strftime("%Y-%m-%d %H:%M:%S") if starttime else "ever"))
