# from rest_framework import status
# from rest_framework.reverse import reverse
# from rest_framework.test import APITestCase
#
# from app_auth.models import ClientInfo, ApiKey
# from app_auth.serializers import ApiKeySerializer
# from app_core.tests.mixins import AuthorizeForTestsMixin
#
#
# class CreateApiKeyAuthTestCase(AuthorizeForTestsMixin, APITestCase):
#     def test_create_api_key_authorized(self):
#
#         response = self.client.post(reverse('api-key-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         client_info = ClientInfo.objects.get()
#         self.assertEqual(client_info.user, self.user)
#         self.assertEqual(client_info.ip_address, '127.0.0.1')
#
#         api_key = ApiKey.objects.get()
#         self.assertEqual(api_key.client_info, client_info)
#         self.assertEqual(api_key.is_active, True)
#         self.assertEqual(response.data, ApiKeySerializer(api_key).data)
#
#
# class CreateApiKeyUnAuthTestCase(APITestCase):
#     def test_create_api_key_unauthorized(self):
#
#         response = self.client.post(reverse('api-key-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         client_info = ClientInfo.objects.get()
#         self.assertEqual(client_info.user, None)
#         self.assertEqual(client_info.ip_address, '127.0.0.1')
#
#         api_key = ApiKey.objects.get()
#         self.assertEqual(api_key.client_info, client_info)
#         self.assertEqual(api_key.is_active, True)
#         self.assertEqual(response.data, ApiKeySerializer(api_key).data)
