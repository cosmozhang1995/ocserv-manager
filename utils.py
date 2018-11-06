def format_number(num, units, floating=None):
  nunits = int(len(units)/2)
  unitstrs = []
  unitvals = []
  unitsteps = []
  for i in range(nunits):
    step = units[i*2+1]
    newnum = int(num / step)
    rem = num - newnum * step
    num = newnum
    unitvals.append(rem)
    unitstrs.append(units[i*2])
    unitsteps.append(step)
  unitvals.append(num)
  unitstrs.append(units[-1])
  unitsteps.append(None)
  if floating is None:
    outstr = ""
    for i in range(nunits+1):
      idx = nunits - i
      if outstr or unitvals[idx] > 0:
        outstr += " %d%s" % (unitvals[idx], unitstrs[idx])
    if not outstr:
      outstr = "0" + unitstrs[0]
    return outstr.strip()
  else:
    for i in range(nunits+1):
      idx = nunits - i
      if unitvals[idx] > 0:
        val = unitvals[idx]
        if idx > 0:
          val2 = float(unitvals[idx-1])/float(unitsteps[idx-1])
          val = float(val) + val2
          valstr = ("%%.%df"%int(floating)) % val
        else:
          valstr = str(val)
        return valstr + unitstrs[idx]
    return "0" + unitstrs[0]

def format_bytes(nbytes):
  return format_number(nbytes, ["B", 1000, "K", 1000, "M", 1000, "G"], 1)

def format_seconds(nsecs):
  return format_number(nsecs, ["s", 60, "m", 60, "h"])