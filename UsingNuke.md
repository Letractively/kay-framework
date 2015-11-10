#How to use nuke comes from http://code.google.com/p/jobfeed/wiki/Nuke

  1. Download bulkkupdate from http://github.com/arachnid/bulkupdate to your project directory.
> > (or create a symlink of bulkupdate in your project directory)
  1. Add kay.ext.nuke to your INSTALLED\_APPS
  1. modify your app.yaml as follows:
```
admin_console:
  pages:
  - name: Bulk Update Jobs
    url: /_ah/bulkupdate/admin/
  - name: Nuke
    url: /_ah/nuke/

handlers:
- url: /_ah/nuke/.*
  script: kay/main.py
  login: admin

- url: /_ah/bulkupdate/admin/.*
  script: bulkupdate/handler.py
  login: admin
```

Thus, you will see Nuke in the left page of your admin console.