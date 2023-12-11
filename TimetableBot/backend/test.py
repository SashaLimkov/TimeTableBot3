from django.test import TestCase
from backend.services.telegram_user import *


class TestBot(TestCase):
    """ """

    def test_01_admin_view(self):
        """Тест представления админки"""

        response = self.client.get("/admin/login/?next=/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django administration', response.content.decode())

    def test_02_bd_req(self):
        """Тест определения профиля по id"""

        prof = get_profile_by_telegram_id(telegram_id=413257908)
        self.assertEqual(prof, 'rakhmatulin8')

    def test_03_notification(self):
        """Тест установки уведомлений"""

        id = 413257908
        user = get_profile_by_telegram_id(telegram_id=id)
        before = user.notification()
        switch_notification(id)
        after = user.notification()
        self.assertNotEqual(before, after)