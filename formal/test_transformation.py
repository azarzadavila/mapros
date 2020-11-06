from rest_framework.test import APITestCase
from rest_framework import status

URL_TRANSFORM = "/text_to_xml/"


class TextToXML(APITestCase):
    def test_correct_sentences(self):
        data = {"sentence": "(A) => (B)"}
        response = self.client.post(URL_TRANSFORM, data, format="json")
        expected = (
            "<sentence>"
            '<binaryConnectorSentence connector="implication">'
            '<constantPredicate symbol="A" />'
            '<constantPredicate symbol="B" />'
            "</binaryConnectorSentence>"
            "</sentence>"
        )
        xml = response.data["xml"].decode()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(xml, expected)
