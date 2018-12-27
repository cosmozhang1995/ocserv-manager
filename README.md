# ocserv-manager

Billing tool for `ocserv`

## Get Start

### How to start

Edit your `ocserv.conf` file, modify:

```
connect-script = /path/to/ocserv-manager/script
disconnect-script = /path/to/ocserv-manager/script
```

Then relaunch `ocserv`

### How to calculate bills

1. Make `config.py` following `config.example.py`
2. Run `python bill-calc.py <username>`. You'll get a hash code for the bill.
3. To mark a bill as paid, run `python bill-pay.py <hash> <paid-amount>`. (`<hash>` can be a short version of the full hash string)
