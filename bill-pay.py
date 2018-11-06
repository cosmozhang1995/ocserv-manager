#!/usr/bin/env python

import sys, os
from logutil import search_log, add_log
from utils import format_bytes, format_seconds
from configs import price_per_gb
import datetime

hashstr = sys.argv[1]
amount = float(sys.argv[2])

now = datetime.datetime.now()

calcrecord = search_log(title="BillCalc", hashstr=hashstr, start=now-datetime.timedelta(hours=24), limit=1).first()
if calcrecord is None:
  raise ValueError("Cannot find the bill log item %s" % hashstr)

totalprice = float(calcrecord.params.get("totalprice"))
if int(amount) < int(totalprice):
  print("[FAILED] Payment (%.2f) less than required price (%.2f) is not accepted" % (amount, totalprice))
  exit(1)

log = add_log(title="BillPay", params=[
    ("calchash",calcrecord.hashstr),
    ("user",calcrecord.params.get("user")),
    ("starttime",calcrecord.params.get("starttime")),
    ("starthash",calcrecord.params.get("starthash")),
    ("endtime",calcrecord.params.get("endtime")),
    ("endhash",calcrecord.params.get("endhash")),
    ("bytesin",calcrecord.params.get("bytesin")),
    ("bytesout",calcrecord.params.get("bytesout")),
    ("duration",calcrecord.params.get("duration")),
    ("totalprice",calcrecord.params.get("totalprice")),
    ("totalpaid",amount)
  ])

print("For user [%s], till <%s>" % (calcrecord.params.get("user"), datetime.datetime.strptime(calcrecord.params.get("starttime"),timefmt).strftime("%Y-%m-%d %H:%M:%S")))
print("  Total price: %s / Paid: %s" % (calcrecord.params.get("totalprice"), amount))
print("  Payment OK.")
