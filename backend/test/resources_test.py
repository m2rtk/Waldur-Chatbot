from unittest import TestCase, main, mock
from common.request import InvalidTokenException
from flask import json
from backend.waldur.waldur import api


def mocked_chatbot_get_response_ok(text):
    return "ok"


def mocked_chatbot_get_response_request(text):
    return "REQUEST"


def mocked_chatbot_get_response_bad_token(text):
    raise InvalidTokenException


def mocked_chatbot_get_response_system_error(text):
    raise Exception


class TestWaldur(TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def assert_correct_response_form(self, response, type="text"):
        for item in response:
            self.assertIn('data', item)
            self.assertIn('type', item)
            self.assertEqual(type, item['type'])

    def test_request_with_no_data_response_error_400(self):
        response = self.app.post("/")
        self.assertEqual(400, response.status_code)
        self.assert_correct_response_form(json.loads(response.get_data()))

    @mock.patch('chatterbot.ChatBot.get_response', side_effect=mocked_chatbot_get_response_ok)
    def test_good_request(self, mock_get):
        response = self.app.post(
            "/",
            data={
                'query': "hello",
                'token': "irrelevant token"
            }
        )
        self.assertEqual(200, response.status_code)
        response = json.loads(response.get_data())
        self.assert_correct_response_form(response)

    @mock.patch('chatterbot.ChatBot.get_response', side_effect=mocked_chatbot_get_response_bad_token)
    def test_bad_token(self, mock_get):
        response = self.app.post(
            "/",
            data={
                'query': "hello",
                'token': "bad token"
            }
        )
        self.assertEqual(401, response.status_code)
        response = json.loads(response.get_data())
        self.assert_correct_response_form(response)

    @mock.patch('chatterbot.ChatBot.get_response', side_effect=mocked_chatbot_get_response_system_error)
    def test_system_error(self, mock_get):
        response = self.app.post(
            "/",
            data={
                'query': "irrelevant",
                'token': "asdqwe123"
            }
        )
        self.assertEqual(500, response.status_code)
        response = json.loads(response.get_data())
        self.assert_correct_response_form(response)


if __name__ == '__main__':
    main()
