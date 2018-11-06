#!/usr/bin/env python

import sys, os
from logutil import search_log
from utils import format_bytes, format_seconds

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
  if record.hashstr.find(starthash) == 0: break
  bytesin += int(record.params.get("bytesin"))
  bytesout += int(record.params.get("bytesout"))
  duration += int(record.params.get("duration"))
hasrecord = (len(records) > 0)

if len(records) > 0:
  starttime = records[-1].time.strftime("%Y-%m-%d %H:%M:%S")
  starthash = records[-1].hashstr
  endtime = records[0].time.strftime("%Y-%m-%d %H:%M:%S")
  endhash = records[0].hashstr
  log = add_log(title="BillCalc", params=[
      ("user",username),
      ("starttime",starttime),
      ("starthash",starthash),
      ("endtime",endtime),
      ("endhash",endhash),
      ("bytesin",bytesin),
      ("bytesout",bytesout),
      ("duration",duration)
    ])

if hasrecord:
  print("Usage for user [%s]:" % username)
  print("  From <%s> to <%s>" % (starttime, endtime))
  print("    Total upload: " + format_bytes(bytesin))
  print("    Total download: " + format_bytes(bytesout))
  print("    Total usage: "+ format_seconds(duration))
else:
  print("No usage for user [%s] since <%s>" % (username, starttime.strftime("%Y-%m-%d %H:%M:%S") if starttime else "ever"))
