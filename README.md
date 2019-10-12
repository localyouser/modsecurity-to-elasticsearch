# ModSecurity JSON to Elasticsearch
forked from theMiddleBlue/modsecurity-to-elasticsearch

### Overview
This program sends MOD_SECURITY inspection logs to Elasticsearch.
Audit Logfile output in JSON format is detected and sent to Elasticsearch by RESTful-API.
The sent log is then deleted.

It is configured to wait until the file is detected, and can be operated as a service using systemd.

### Usage
```bash
python modsec_parser.py -d <auditlog directory>
```

### Prerequisites 
* yajl-dev must be installed.
* You need to build mod_security with --with-yajl.
* The following settings are required in modsecurity.conf.
** SecAuditEngine RelevantOnly
** SecAuditLogRelevantStatus "^[0-9]+"
** SecAuditLogType concurrent
** SecAuditLogFormat JSON
** SecAuditLogStorageDir <auditlog directory>

### Reference
[https://medium.com/@themiddleblue/modsecurity-elasticsearch-kibana-40e4f8191e35](https://medium.com/@themiddleblue/modsecurity-elasticsearch-kibana-40e4f8191e35)
[https://www.bluecore.net/2019/10/12/security-pythonmod_security%e3%81%ae%e6%a4%9c%e5%87%ba%e7%8a%b6%e6%85%8b%e3%82%92%e5%8f%af%e8%a6%96%e5%8c%96%e3%81%99%e3%82%8b/](https://www.bluecore.net/2019/10/12/security-pythonmod_security%e3%81%ae%e6%a4%9c%e5%87%ba%e7%8a%b6%e6%85%8b%e3%82%92%e5%8f%af%e8%a6%96%e5%8c%96%e3%81%99%e3%82%8b/)

### Execution environment
* Hardware: Virtual Machine(4vCPU/6GB RAM/240GB VHD/ESXi6.5Update3)
* OS: CentOS7
* HTTP Server: Nginx 1.17.3(Souce-Compiled)
* Mod_Security: ModSecurity v3.0.3 (Linux/Source-Compiled)
* Core Rule Set: OWASP_CRS/3.2.0
* Elasticsearch: 5.6.16

