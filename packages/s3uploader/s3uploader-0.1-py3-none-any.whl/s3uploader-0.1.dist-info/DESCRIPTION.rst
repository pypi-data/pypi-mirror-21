S3Uploader
==========

A simple application to upload files to an Amazon S3 bucket. Behind the scenes this script uses the awesome Boto3
library to access the Amazon Web Services.

Quickstart
----------
The application uses the AWS credentials file located in ~/.aws/credentials

    usage: s3uploader.py [-h] [--verbose] [--store-paths] bucket file [file ...]

    Upload files to an Amazon S3 bucket

    positional arguments:
      bucket         Name of the S3 bucket to use
      file           File to upload to the S3 bucket

    optional arguments:
      -h, --help     show this help message and exit
      --verbose      Give verbose output while uploading files
      --store-paths  Store the file path in the S3 object name


Options
-------

--store-paths
    If this flag is set the S3 object will stored with the path you specify, otherwise the filenamewill be used as the
    object name. Using this approach it is possible to simulate a directory structure on S3.

--verbose
    Give verbose output while uploading files to S3.

