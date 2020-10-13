import logging
from unittest import TestCase
import requests_mock
from parameterized import parameterized, param
from hvac import adapters

class TestActions(TestCase):
    @parameterized.expand([
        param(
            "Standard Vault Adrress",
            url="http://localhost:8200",
        ),
    ])

    def test_get(self, url, path='v1/sys/health', redirect_url=None):
        path = path.replace('//', '/')
        expected_status_code = 200
        mock_url = '{0}/{1}'.format(url, path)
        expected_request_urls = [mock_url]
        adapter = adapters.Request(base_uri=url)
        response_headers = {}
        response_status_code = 200
        with requests_mock.mock() as requests_mocker:
            logging.debug('Registering mock url %s' % mock_url)
            requests_mocker.register_uri(
                method='GET',
                url=mock_url,
                headers=response_headers,
                status_code=response_status_code,
            )
            response = adapter.get(
                url=path,
            )
            # Assert all our expected uri(s) were requested
            for request_num, expected_request_url in enumerate(expected_request_urls):
                self.assertEqual(
                    first=expected_request_url,
                    second=requests_mocker.request_history[request_num].url
                )
            self.assertEqual(
                first=expected_status_code,
                second=response.status_code,
            )