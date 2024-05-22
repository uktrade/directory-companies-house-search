from django.contrib.auth import get_user_model
from django.db import DatabaseError


class DatabaseHealthCheck:
    name = 'database'

    def check(self):
        try:
            User = get_user_model()
            User.objects.all().exists()
        except DatabaseError as de:
            return False, de
        else:
            return True, ''


health_check_services = (DatabaseHealthCheck,)
