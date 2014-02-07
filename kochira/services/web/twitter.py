"""
Twitter timeline follower.

Broadcasts a Twitter user's timeline into IRC. Provides tweeting capabilities as well as
Markov-chain text generation with a compatible Brain.

Configuration Options
=====================

``oauth``
  Dictionary containing the OAuth key, secret, token, and token secret.
  e.g. ``{"key": "qwerty", "secret": "123456", "token": "nekot", "token_secret": "nekot_sekrit"}``

``announce``
  List of announce channels, e.g.
  ``[{"network": "#freenode", "channel": "kochira"}]``.

Commands
========

Tweet
-----

::

    $bot: tweet <tweet>
    !tweet <tweet>

**Requires permission:** tweet

Tweet the given text.

Reply
-----

::

    $bot: reply to <ID> with <tweet>
    !reply <ID>

**Requires permission:** tweet

Reply to the given tweet. Automatically prepends the appropriate @mention. If no tweet is given,
attemps to search for a usable Brain service and uses it to generate a suitable reply.
"""

import time
from threading import Thread
from twitter import Twitter, TwitterStream, OAuth
from kochira.service import Service

import logging
logger = logging.getLogger(__name__)

service = Service(__name__, __doc__)

@service.setup
def make_twitter(bot):
    storage = service.storage_for(bot)
    config = service.config_for(bot)
    o = config["oauth"]

    storage.api = Twitter(auth=OAuth(o["token"], o["token_secret"], o["key"], o["secret"]))
    storage.active = True
    storage.stream = Thread(target=_follow_userstream, args=(bot,), daemon=True)
    storage.stream.start()

@service.shutdown
def kill_twitter(bot):
    storage = service.storage_for(bot)
    storage.active = False
    storage.stream.join()

def _follow_userstream(bot):
    o = service.config_for(bot)["oauth"]
    stream = TwitterStream(auth=OAuth(o["token"], o["token_secret"], o["key"], o["secret"]), domain='userstream.twitter.com', block=False)

    for msg in stream.user():
        if msg is not None:
            logger.debug(str(msg))

            # Twitter signals start of stream with the "friends" message.
            if 'friends' in msg:
                _announce(bot, "\x02twitter:\x02 This channel is now streaming Twitter in real-time.")
            elif 'text' in msg and 'user' in msg:
                url_format = "(https://twitter.com/{0[user][screen_name]}/status/{0[id_str]})"
                if 'retweeted_status' in msg:
                    text = "\x02[@{0[user][screen_name]} RT {0[retweeted_status][user][screen_name]}]\x02 {0[retweeted_status][text]} " + url_format
                else:
                    text = "\x02[@{0[user][screen_name]}]\x02 {0[text]} " + url_format

                _announce(bot, text.format(msg))
        else:
            time.sleep(.5)

        if not service.storage_for(bot).active:
            break

def _announce(bot, text):
    for announce in service.config_for(bot)["announce"]:
        bot.networks[announce["network"]].message(announce["channel"], text)
