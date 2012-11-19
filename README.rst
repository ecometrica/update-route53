==========================
 Update Amazon's Route 53
==========================

**update-route53** is designed to automatically update your Route 53
configuration when one of your Amazon EC2 instances gets a new IP.

With a proper configuration, the instance's hostname will have its
CNAME record updated to point to its EC2 hostname. This makes the
hostname resolve to the public or private IP address, depending on
whether you are resolving from within the EC2 network.


Installation
============

You can get a copy of the source by using::

    $ git clone https://github.com/ecometrica/update-route53.git

Note that this program requires Python 2.6 or higher.

Next, install the program into your root directory of your EC2 instance::

    $ sudo install -d -m 0700 -o root -g root /root/bin/
    $ sudo install -m 0700 -o root -g root update-route53.py /root/bin/update-route53.py


Boto
----

We rely on boto_ to talk to Amazon Web Services.

Under Debian or Ubuntu, run the following to install it::

    $ sudo apt-get install python-boto


Amazon Web Services
-------------------

Make sure you have an Amazon Web Services (AWS) user which can access
your Route 53 configuration:

1. Go to your AWS control panel and select the **IAM** service.

2. Click on the **Users** tab and create or select a user.

3. In the **Permissions** tab, attach a policy that gives the
   following permissions::

    {
        "Statement": [
            {
                "Effect":"Allow",
                "Action":"s3:ListAllMyBuckets",
                "Resource":"arn:aws:s3:::*"
            },{
                "Effect":"Allow",
                "Action":"route53:ListHostedZones",
                "Resource":"*"
            },{
                "Effect":"Allow",
                "Action":"route53:GetHostedZone",
                "Resource":"arn:aws:route53:::*"
            },{
                "Effect":"Allow",
                "Action":"route53:ListResourceRecordSets",
                "Resource":"arn:aws:route53:::*"
            },{
                "Effect":"Allow",
                "Action":"route53:ChangeResourceRecordSets",
                "Resource":"arn:aws:route53:::*"
            }
        ]
    }

Create a ``/root/.boto`` configuration file containing::

    [Credentials]
    aws_access_key_id = *AWS Access Key*
    aws_secret_access_key = *AWS Secret Key*

Make sure the ``/root/.boto`` file has the right permissions. Under
Unix, you'll want::

    $ sudo chmod 0600 /root.boto

    

Debian and Ubuntu
-----------------

In order to get your system to update its DNS records when its IP
addresses change, you need to install an ``if-up`` hook::

    $ sudo install -m 0755 -o root -g root debian/update-route53 /etc/network/if-up.d/


Reporting bugs and submitting patches
=====================================

Please check our `issue tracker`_ for known bugs and feature requests.

We accept pull requests for fixes and new features.


Credits
=======

Maxime Dupuis and Simon Law wrote this program, with the generous
support of Ecometrica_.

.. _boto: https://github.com/boto/boto
.. _issue tracker: https://github.com/ecometrica/update-route53/issues
.. _Ecometrica: http://ecometrica.com/
