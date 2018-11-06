import os
import datetime

maxfilesize = 1024*1024*16
timefmt = "%Y-%m-%dT%H:%M:%S"

currdir = os.path.realpath(os.path.dirname(__file__))
logdir = os.path.join(currdir, "logs")
if not os.path.isdir(logdir): os.mkdir(logdir)
logpath = os.path.join(logdir, "stats.log")

def _get_histlogs():
  import re
  histlogs = os.listdir(logdir)
  histlogs = list(map(lambda x: (x, re.match(r"stats\.(\d+)\.log", x)), histlogs))
  histlogs = list(filter(lambda x: not x[1] is None, histlogs))
  histlogs = list(map(lambda x: (x[0], int(x[1].group(1))), histlogs))
  histlogs = list(sorted(histlogs, key=(lambda x: x[1])))
  return histlogs

def _get_logfiles():
  logfiles = list(map(lambda x: x[0], _get_histlogs()))
  if os.path.exists(logpath): logfiles.append("stats.log")
  return logfiles

class LogParams:
  def __init__(self, initval):
    if isinstance(initval, dict): initval = [(k,initval[k]) for k in initval]
    elif isinstance(initval, LogParams): initval = initval.paramlist
    self.paramlist = initval
  def get(self, name):
    for item in self.paramlist:
      if item[0] == name:
        return item[1]
    return None
  def set(self, name, value):
    for item in self.paramlist:
      if item[0] == name:
        item[1] = value
        return
    self.paramlist.append(item)
  def __str__(self):
    return " ".join([("%s=%s" % (x[0],x[1])) for x in self.paramlist])
  def keys(self):
    return [x[0] for x in self.paramlist]

class LogItem:
  def __init__(self, hashstr=None, time=None, title=None, params=None, rawline=None):
    self.hashstr = hashstr
    self.time = time
    self.title = title
    self.params = params
    self.rawline = rawline

def parse_log_line(content):
  words = content.split(" ")
  words = list(map(lambda x: x.strip(), words))
  words = list(filter(lambda x: len(x) > 0, words))
  hashstr = words[0]
  time = datetime.datetime.strptime(words[1], "%Y-%m-%dT%H:%M:%S")
  title = words[2][1:-1]
  params = LogParams([tuple(x.split("=")) for x in words[3:]])
  return LogItem(hashstr=hashstr, time=time, title=title, params=params, rawline=content)

def add_log(title=None, params=None, time=None):
  import hashlib
  if time is None: time = datetime.datetime.now()
  paramstr = str(LogParams(params))
  echostr = "%s [%s] %s" % (time.strftime(timefmt), title, paramstr)
  echostr = hashlib.md5(echostr).hexdigest() + " " + echostr
  if os.path.exists(logpath):
    filesize = os.path.getsize(logpath)
    if filesize >= maxfilesize:
      histlogs = _get_histlogs()
      nextidx = (histlogs[-1][1]+1) if (len(histlogs)>0) else 1
      nextpath = os.path.join(logdir, "stats.%d.log"%nextidx)
      os.rename(logpath, nextpath)
  f = open(logpath, "a")
  f.write(echostr + "\n")
  f.close()
  return parse_log_line(echostr)

class SearchResult(list):
  def first(self):
    if len(self) > 0:
      return self[0]
    else:
      return None

def search_log(hashstr=None, title=None, time=None, start=None, end=None, judgement=None, limit=None, desc=True, **kwargs):
  if not limit is None and limit <= 0: return SearchResult([])
  if isinstance(time, str): time = datetime.datetime.strptime(time,timefmt)
  if isinstance(start, str): start = datetime.datetime.strptime(start,timefmt)
  if isinstance(end, str): end = datetime.datetime.strptime(end,timefmt)
  logfiles = _get_logfiles()
  logfiles = [os.path.join(logdir, filename) for filename in logfiles]
  nlogfiles = len(logfiles)
  # get list of the files to search into
  startidx = None
  endidx = None
  for i in range(nlogfiles):
    filepath = logfiles[i]
    f = open(filepath)
    firstline = ""
    while len(firstline) == 0:
      firstline = f.readline()
      if len(firstline) == 0: break
      firstline = firstline.strip()
    f.close()
    if len(firstline) > 0:
      firstitem = parse_log_line(firstline)
      if startidx is None and start and firstitem.time >= start:
        startidx = max(0, i-1)
      if end and firstitem.time > end:
        endidx = i
        break
  if startidx is None: startidx = 0
  if endidx is None: endidx = nlogfiles
  # do the search
  retitems = []
  for i in range(nlogfiles):
    fileidx = (nlogfiles - i - 1) if desc else i;
    if fileidx < startidx or fileidx >= endidx: continue
    filepath = logfiles[fileidx]
    f = open(filepath)
    lines = f.read().split("\n")
    f.close()
    nlines = len(lines)
    for j in range(nlines):
      line = lines[(nlines - j - 1) if desc else j].strip()
      if len(line) == 0: continue
      item = parse_log_line(line)
      if judgement and not judgement(item): continue
      if hashstr and item.hashstr.find(hashstr) != 0: continue
      if title and item.title != title: continue
      if time and item.time != time: continue
      if start and item.time < start: continue
      if end and item.time > end: continue
      kwargmismatch = False
      for k in kwargs:
        if item.params.get(k) != kwargs[k]:
          kwargmismatch = True
          break
      if kwargmismatch: continue
      retitems.append(item)
      if not limit is None and len(retitems) >= limit: break
    if not limit is None and len(retitems) >= limit: break
  return SearchResult(retitems)



