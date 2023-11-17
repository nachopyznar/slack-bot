import os
import schedule
import time
import logging

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


def send_message(client, message, slack_members):
    # make the POST request through the python slack client and check if the request was a success
    logging.info("sending message")
    try:
        for member in slack_members:
            if not member["is_bot"]:
                client.chat_postMessage(
                    channel=member["id"],
                    text=message
                )  # .get()
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)


if __name__ == "__main__":

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    slack_client = WebClient(SLACK_BOT_TOKEN)
    logging.debug("authorized slack client")

    # Send the message to every member of the Slack organization
    members = slack_client.users_list().get("members")

    msg = "" \
          "Hola Bella Team! @aquí " \
          "\n Recuerden cargar todas las horas que estuvieron trabajando en JIRA :rezo: " \
          "\n !!!Muchas Gracias!" \
          ""

    schedule.every().friday.at("12:00").do(lambda: send_message(slack_client, msg, members))

    logging.info("entering loop")

    while True:
        schedule.run_pending()
        time.sleep(5)  # sleep for 5 seconds between checks on the scheduler