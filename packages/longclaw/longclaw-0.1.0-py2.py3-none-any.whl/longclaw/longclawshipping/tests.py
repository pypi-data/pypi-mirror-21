from longclaw.tests.utils import LongclawTestCase


class AddressTest(LongclawTestCase):
    def test_create_address(self):
        """
        Test creating an address object via the api
        """
        data = {
            'name': 'Bob Testerson',
            'line_1': 'Bobstreet',
            'city': 'Bobsville',
            'postcode': 'BOB22 2BO',
            'country': 'UK'
        }
        self.post_test(data, 'longclaw_address_list')
