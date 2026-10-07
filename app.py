import os
from dotenv import load_dotenv
from pullData import pullHeroData
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import services as Serv


# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started

load_dotenv()
bot_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')

# Initializes your app with your bot 
app = App(token=bot_token)
SocketModeHandler(app, app_token)

user_packages = {}

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.message("Init match") #change to real; when i need
def initMatch(say):
    say(
        blocks=[
        {
            "type": "section",
            "text": {"type": 'mrkdwn', "text": f"Would you like to start a match instance"},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Start Match"},
                "action_id": "startMatch",
            },
        }
        ],
        text=f"Would you like to start a match instance"
    )

@app.action("startMatch")
def startMatch(ack, body, say):
    ack()
    user = body['user']['id']
    user_packages[user] = {'stage': 0}
    say("List relevant info in this format:\n"
    "'postion, draft order, [enemy1, enemy2, etc]'")

@app.message("")
def receive_match_info(message, say):
    user_id = message['user']
    if user_id not in user_packages:
        return
    if user_packages[user_id]['stage'] == 0:
        match_info = message['text']
        say(f"received your match information: \n{match_info}")
        user_packages[user_id]['stage'] = 1
        Pos, draftOrder, enemyPack = Serv.parse_mI(match_info)
        heroes = enemyPack.split(",")
        heroes[0] = heroes[0].strip().strip("[")
        heroes[-1] = heroes[-1].strip().strip(']')
    
        matchSession = {}
        for hero in heroes:
            print(hero)
            matchSession[hero] = {}
            matchups = pullHeroData(hero)
            winrates = Serv.calc_winrate(matchups)
            matchSession[hero]['winrate'] = winrates

        averages = Serv.calc_avgs(matchSession)
        bestPicks = Serv.find_bestPick(averages)

        message = "Top 5 Counter Picks*\n\n"

        for i in range(len(bestPicks)):
            message += f"{i + 1}. {bestPicks[i]['hero']} -- {bestPicks[i]['winrate']} Winrate\n"

        say(message)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
