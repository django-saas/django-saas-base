from saas_base.test import SaasTestCase
from tests.demo_app.models import UserProfile


class TestUserAPI(SaasTestCase):
    user_id = SaasTestCase.GUEST_USER_ID

    def test_get_current_user(self):
        self.force_login()
        url = '/m/user/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNone(data['picture'])

        UserProfile.objects.create(user_id=self.user_id, picture='https://example.com/avatar.jpg')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['picture'], 'https://example.com/avatar.jpg')

    def test_update_user(self):
        self.force_login()
        payload = {'first_name': 'First', 'picture': 'https://example.com/avatar2.jpg'}
        resp = self.client.patch('/m/user/', data=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['first_name'], 'First')
        self.assertEqual(data['picture'], 'https://example.com/avatar2.jpg')

        payload = {'last_name': 'Last', 'picture': 'https://example.com/avatar3.jpg'}
        resp = self.client.patch('/m/user/', data=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['first_name'], 'First')
        self.assertEqual(data['last_name'], 'Last')
        self.assertEqual(data['picture'], 'https://example.com/avatar3.jpg')
