import os
import datetime

currdir = os.path.realpath(os.path.dirname(__file__))
logpath = os.path.join(currdir, "scription.log")

reason = os.environ["REASON"]
is_disconn = (reason == "disconnect")
is_connect = (reason == "connect")
username = os.environ["USERNAME"]
ip_real = os.environ["IP_REAL"]
if is_disconn:
  bytesin = int(os.environ["STATS_BYTES_IN"])
  bytesout = int(os.environ["STATS_BYTES_OUT"])
  duration = int(os.environ["STATS_DURATION"])
now = datetime.datetime.now()

echostr = "%s [Connect] user=%s ip=%s" % (now.strftime("%Y-%m-%dT%H:%M:%S"), username, ip_real)
if is_disconn:
  echostr += " bytesin=%d bytesout=%d duration=%d" % (bytesin, bytesout, duration)
echostr += "\n"

f = open(logpath, "a")
f.write(echostr)
f.close()
