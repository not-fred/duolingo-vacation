import logging
import sys
import os
import duolingo

config = {}
configLoadFailed = False

username = os.environ.get('DUO_USERNAME')
password = os.environ.get('DUO_PASSWORD')
logFile  = os.environ.get('DUO_LOG_FILE')


logConfig = {
    "format": "%(asctime)s [%(levelname)s] %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO
}

if logFile is None:
    logConfig["stream"] = sys.stdout
else:
    logConfig["filename"] = logFile

logging.basicConfig(**logConfig)

if username is None or password is None:
    logging.error(
        "Please set the environment configurations 'DUO_USERNAME' to the username and 'DUO_PASSWORD' to the password of your Duolingo account. " +
        "See https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard for instructions."
    )
else:
    try:
        lingo = duolingo.Duolingo(
            username = username,
            password = password
        )
    except Exception as e:
        logging.error(e)
        sys.exit()
    streakInfo = lingo.get_streak_info()
    try:
        streakBought = lingo.buy_streak_freeze()
        streakText = f"Streak freeze {'bought' if streakBought else 'exists'}"
    except Exception as e:
        streakText = "Insufficient lingots to purchase streak freeze"
    logging.info(f"Currently on a {streakInfo['site_streak']} day streak. {streakText}.")
