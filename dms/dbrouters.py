from dms.models import *

class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        if model == Admin:
            return 'system'
        if model == user:
            return 'system'
        if model == signup:
            return 'system'
        if model == ImageModel:
            return 'system'
        if model == aadharQ:
            return 'system'
        if model == pancardQ:
            return 'system'
        if model == licenceQ:
            return 'system'
        if model == RationQ:
            return 'system'
        if model == voteridQ:
            return 'system'
        if model == userlogin:
            return 'system'
        if model == signup1:
            return 'system'
        return None

    def db_for_write(self, model, **hints):
        if model == Admin:
            return 'system'
        if model == user:
            return 'system'
        if model == signup:
            return 'system'
        if model == ImageModel:
            return 'system'
        if model == aadharQ:
            return 'system'
        if model == pancardQ:
            return 'system'
        if model == licenceQ:
            return 'system'
        if model == RationQ:
            return 'system'
        if model == voteridQ:
            return 'system'
        if model == userlogin:
            return 'system'
        if model == signup1:
            return 'system'
        return None