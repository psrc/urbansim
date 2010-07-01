# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010 University of California, Berkeley
# See opus_core/LICENSE

import logging
import os

logging.basicConfig(level=logging.ERROR)

CAMELOT_ATTACHMENTS = ''
# media root needs to be an absolute path for the file open functions
# to function correctly
CAMELOT_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

REPOSITORY = 'repository'
ENGINE = lambda:'sqlite:///zone.db'

def setup_model():
    #import camelot.model
    from elixir import setup_all
    import model
    setup_all(create_tables=True)
    from camelot.model.authentication import updateLastLogin
    updateLastLogin()
