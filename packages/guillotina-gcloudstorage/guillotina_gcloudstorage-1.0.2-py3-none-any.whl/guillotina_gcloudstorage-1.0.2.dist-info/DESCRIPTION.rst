.. contents::

GUILLOTINA_GCLOUDSTORAGE
========================

GCloud blob storage for guillotina.


Example config.json entry:

    "utilities": {
        "provides": "guillotina_gcloudstorage.interfaces.IGCloudBlobStore",
        "factory": "guillotina_gcloudstorage.storage.GCloudBlobStore",
        "settings": {
            "json_credentials": "/path/to/credentials.json",
            "bucket": "name-of-bucket"
        }
    }

1.0.2 (2017-04-26)
------------------

- Need to be able to provide loop param in constructor of utility
  [vangheem]


1.0.1 (2017-04-25)
------------------

- Compatibility fixes with aiohttp 2
  [vangheem]


1.0.0 (2017-04-24)
------------------

- initial release


