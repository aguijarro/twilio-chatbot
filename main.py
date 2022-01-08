import logging
import requests
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)


def whatsapp_webhook(request):
    """HTTP Cloud Function.
    Parameters
    ----------
    request (flask.Request) : The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns
    -------
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    country = request.values.get('Body', "").lower()
    resp = requests.get(f'https://restcountries.com/v3.1/name/{country}?fullText=true')
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    if not (200 <= resp.status_code <= 299):
        logger.error(
            f'Failed to retrieve data for the following country - {country.title()}. Here is a more verbose reason {resp.reason}'
        )
        msg.body(
            'Sorry we could not process your request. Please try again or check a different country'
        )
    else:
        data = resp.json()[0]
        common_name = data['name']['common']
        official_name = data['name']['official']

        msg.body(
            f"{common_name} is a country which official name is {official_name}."
        )
    return str(twilio_response)
