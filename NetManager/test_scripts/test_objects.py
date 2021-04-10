"""

Creates object instances for use in unit testing

"""
from django.contrib.auth.models import User
from devices.models import Device


# creates a test user for unit tests
def create_test_user(self):
    # create test user
    self.username = 'test'
    self.password = 'test'
    self.user = User(username=self.username, password=self.password)
    self.user.set_password(self.password)
    self.user.save()
    return self


# creates a test device for unit tests
def create_test_device(self, user):
    # create test device
    self.device = Device.objects.create(
        pk=1,
        user=user,
        name='device_test',
        type='test_device',
        host='1.1.1.1',
        vendor='Cisco',
        location='',
        contact='',
        status=False,
    )
    return self
