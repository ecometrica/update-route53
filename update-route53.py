#!/usr/bin/env python

from __future__ import unicode_literals

from socket import getfqdn
import sys
from urllib import urlopen

from boto.route53.connection import Route53Connection


INSTANCE_METADATA_URL = 'http://169.254.169.254/latest/meta-data/'


def get_metadata(key, url=INSTANCE_METADATA_URL):
    return urlopen(url + key).read()


def set_cname(cname, name):
    hostname, domain = cname.split('.', 1)

    conn = Route53Connection()
    zone = conn.get_hosted_zone_by_name(domain)
    if zone is None:
        raise ValueError('Invalid CNAME: {0}'.format(cname))

    if not cname.endswith('.'):
        cname += '.'

    records = conn.get_all_rrsets(hosted_zone_id=zone.Id.split('/')[-1])

    # Remove old CNAMEs if they exist
    old_cnames = [r for r in records if r.name == cname and r.type == 'CNAME']
    for old in old_cnames:
        change = records.add_change(action='DELETE',
                                    name=old.name,
                                    type=old.type)
        change.__dict__.update(old.__dict__)

    # Add current CNAME
    change = records.add_change(action='CREATE',
                                name=cname,
                                type='CNAME',
                                ttl=60)
    change.add_value(name)
    records.commit()


def update_dns():
    set_cname(cname=getfqdn(),
              name=get_metadata(key='public-hostname'))


# Provide get_hosted_zone_by_name if it doesn't already exist
if not hasattr(Route53Connection, 'get_hosted_zone_by_name'):
    def get_hosted_zone_by_name(self, hosted_zone_name):
        if hosted_zone_name[-1] != '.':
            hosted_zone_name += '.'
        all_hosted_zones = self.get_all_hosted_zones()
        for zone in all_hosted_zones['ListHostedZonesResponse']['HostedZones']:
            #check that they gave us the FQDN for their zone
            if zone['Name'] == hosted_zone_name:
                return self.get_hosted_zone(zone['Id'].split('/')[-1])
    Route53Connection.get_hosted_zone_by_name = get_hosted_zone_by_name

if __name__ == '__main__':
    update_dns()
    sys.exit(0)
