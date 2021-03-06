import redis

from django.conf import settings
from django.core import management
from django.test import TestCase


class AutocompleterTestCase(TestCase):
    def setUp(self):
        self.redis = redis.Redis(host=settings.AUTOCOMPLETER_REDIS_CONNECTION['host'],
            port=settings.AUTOCOMPLETER_REDIS_CONNECTION['port'],
            db=settings.AUTOCOMPLETER_REDIS_CONNECTION['db'])

        # purge any possible old test data in case of previous failures where tearDown didn't fire.
        # This is hardcoded so you don't accidentally wipe your redis db somehow.
        old_data = self.redis.keys("djac.test.*")
        pipe = self.redis.pipeline()
        for i in old_data:
            pipe.delete(i)
        pipe.execute()

    @classmethod
    def tearDownClass(cls):
        super(AutocompleterTestCase, cls).tearDownClass()
        management.call_command('flush', verbosity=0, interactive=False)
