====
Cull
====

Cull provides a very specific cli tool to parse boto3 output. Usage can viewed by
running the tool via cli::

    cull


EC2
===

Instance Name Tags are expected to use the following
naming convention::

    <cloud>_<service>_*

How to
------

To parse EC2 instances with Name tags like *production_app_**::

    cull ec2 production app


S3
==

A list tool to list or delete root level S3 buckets

List
----

To list all root level buckets with a specific string in the name::

    cull s3list production

Delete
------

To delete a root level bucket **AND ALL CONTENTS WITHIN**::

    cull s3delete bucketname

You will be prompted before delete function is executed