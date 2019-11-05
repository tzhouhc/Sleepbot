# Sleepbot

Sleeps.

## Dependencies

* discord.py
* cachetools

## Invoke

1. Create a json config file, e.g. `config.json`.

2. Put bot token and easter hen url in it: 

```json
{
  "token": "asdfasdfasdfasdf",
  "easter_hen_url": "https://docs.google.com/spreadsheets/d/DOCID/export?format=csv"
}
```

3. Run `./bot.py -c config.json`.

4. Alternatively make the bot a systemd service:

```systemd
[Unit]
Description=Sleepbot Service
Wants=network.target
After=network.target

[Service]
User=ting
Nice=5
KillMode=process

WorkingDirectory=/home/ting/dev/Sleepbot
ExecStart=/usr/bin/python3 ./bot.py -c config.json

Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
