# ModSecurity JSON to Elasticsearch
please, read the following post before using it:
[coming soon](#)

### Usage:
```bash
python modsec_parser.py -d <auditlog directory>
```

### Example:
```
$ python modsec_parser.py -d /usr/local/nginx/logs/modsecurity/www.example.com
Parsed /usr/local/nginx/logs/modsecurity/www.example.com/20171114/20171114-1714/20171114-171410-151067605036.512983
Sleeping for a while...
```

or run it in background

```
$ python modsec_parser.py -d /usr/local/nginx/logs/modsecurity/www.example.com > /dev/null 2>&1 &
```

### Contributors
probably your python skill are better then mine, so all contributions are appreciated :)

