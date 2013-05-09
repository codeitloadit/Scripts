'''
Created on May 13, 2011

@author: chris
'''
# One-off script to fix Manor's addresses in the database.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

os.environ['PYTHONPATH'] = '.'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from orpheus.associations.models import Association
from orpheus.associations.models import AssociationProfile
from orpheus.customers.models import Customer, Address


customer = Customer.objects.get(slug__exact='massingham')
result = Association.objects.filter(customer=customer)
associations = []
err_associations = []
for row in result:
    try:
        associations.append(row.get_profile())
    except AssociationProfile.DoesNotExist:
        err_associations.append(row)

used_addresses = []
for assoc in associations:
    if not assoc.return_address:
        continue
    if assoc.return_address not in used_addresses:
        used_addresses.append(assoc.return_address)
    else:
        new_address = assoc.return_address
        new_address.id = None
        new_address.save()
        assoc.return_address = new_address
        assoc.save()
        
    if not assoc.return_address.line_1:
        assoc.return_address.line_1 = assoc.return_address.line_2
        assoc.return_address.line_2 = ''
        assoc.return_address.save() 

    if not assoc.return_address:
        continue

    if assoc.return_address not in used_addresses:
        used_addresses.append(assoc.return_address)
    else:
        new_address = assoc.return_address
        new_address.id = None
        new_address.save()
        assoc.return_address = new_address
        assoc.save()
        
    if not assoc.return_address.line_1:
        assoc.return_address.line_1 = assoc.return_address.line_2
        assoc.return_address.line_2 = ''
        assoc.return_address.save()