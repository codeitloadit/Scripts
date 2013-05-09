import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

os.environ['PYTHONPATH'] = '.'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from orpheus.associations.models import AssociationProfile

invalid_numbers = list()

def normalize(value):
    if not value:
        return value 
        
    result = ''
    for char in value:
        if ord(char) >= ord('0') and ord(char) <= ord('9'):
            result += char
            
    if len(result) != 10:
        invalid_numbers.append('{0} | {1}'.format(i, value))
        return value
        
    return result[:3] + '-' + result[3:6] + '-' + result[6:]
        
        
profiles = AssociationProfile.objects.exclude(contact_phone=u'', contact_fax=u'')

for i, profile in enumerate(profiles):
    print '{0} | {1} | {2} | {3}'.format(i, profile.id, normalize(profile.contact_phone), normalize(profile.contact_fax))
    
if invalid_numbers:
    print '\nInvalid numbers found:'
    
    for number in invalid_numbers:
        print number
            
if raw_input('\nProceed with update? [y/n]: ') == 'y':
    count = len(profiles)
    for i, profile in enumerate(profiles):
        percent = (i * 100) / count
        sys.stdout.write('{0}%'.format(percent))
        sys.stdout.write('\r')
        sys.stdout.flush()
        
        profile.contact_phone = normalize(profile.contact_phone)
        profile.contact_fax = normalize(profile.contact_fax)
        profile.save()

    print 'Done!\n'

        