import logging
import os
from sqlalchemy import *

logging.basicConfig(level=logging.ERROR)

CAMELOT_ATTACHMENTS = ''
# media root needs to be an absolute path for the file open functions
# to function correctly
CAMELOT_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

REPOSITORY = 'repository'
ENGINE = lambda:'sqlite:///sample_parcel.sqlite'

def setup_model():
    #import camelot.model
    from elixir import setup_all
    import model
    print 'Testing...'
    print 'model.metadata: ', model.__metadata__

    setup_all(create_tables=False)
    print 'Original Tables:'
#    for table in model.__metadata__.sorted_tables:
#        print str(table)
    tables_to_drop = ([
        'address',
#        'authentication_mechanism',
#        'authentication_mechanism_username',
        'batch_job',
        'batch_job_type',
        'contact_mechanism',
        'fixture',
        'fixture_version',
        'geographic_boundary',
        'geographic_boundary_city',
        'geographic_boundary_country',
        'memento',
        'memento_create',
        'memento_delete',
        'memento_update',
        'organization',
        'party',
        'party_address',
        'party_address_role_type',
        'party_authentication',
        'party_contact_mechanism',
        'party_relationship',
        'party_relationship_dir',
        'party_relationship_empl',
        'party_relationship_shares',
        'party_relationship_suppl',
        'party_representor',
        'party_status',
        'party_status_type',
        'person',
        'synchronizedable',
        'synchronized',
        'synchronizedable_to_synchronized',
#        'translation',
        ])
    for table in model.__metadata__.sorted_tables:
        if str(table) in tables_to_drop:
            model.__metadata__.remove(table)
    setup_all(create_tables=True)
#    print
#    print 'Reduced Tables'
#    for table in model.__metadata__.sorted_tables:
#        print str(table)
       
    from camelot.model.authentication import updateLastLogin
    updateLastLogin()
