.. contents::

GUILLOTINA_S3STORAGE
====================

S3 blob storage for guillotina.


Example config.json:

    "utilities": [{
        "provides": "guillotina_s3storage.interfaces.IS3BlobStore",
        "factory": "guillotina_s3storage.storage.S3BlobStore",
        "settings": <aws-credentials>
    }]

1.0.2 (2017-04-26)
------------------

- utility needs to be able to take loop param
  [vangheem]


1.0.1 (2017-04-25)
------------------

- Compabilities with latest aiohttp
  [vangheem]


1.0.0 (2017-04-24)
------------------

- initial release


