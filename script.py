import os
import datetime
from logutil import add_log

reason = os.environ["REASON"]
is_disconn = (reason == "disconnect")
is_connect = (reason == "connect")
username = os.environ["USERNAME"]
ip_real = os.environ["IP_REAL"]
if is_disconn:
  bytesin = int(os.environ["STATS_BYTES_IN"])
  bytesout = int(os.environ["STATS_BYTES_OUT"])
  duration = int(os.environ["STATS_DURATION"])

if is_disconn: title = "Disconnect"
if is_connect: title = "Connect"

params = [];
params.append(("user", username))
params.append(("ip", ip_real))
if is_disconn:
  params.append(("bytesin", bytesin))
  params.append(("bytesout", bytesout))
  params.append(("duration", duration))

add_log(title=title, params=params)
