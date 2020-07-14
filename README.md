# ranking-bot
This bot is intended to provide statistics and manage general scoreboard info.
## How to Rank 
same = sum(total amount of ranks - user rank)/total amount of games
| All | X-Mage | IRL/Budget|
| --- | ------ | ---------- |
| same | same | same |
## Who Gets to be Ranked
### ideas
- player must play x games
- player must play every person atleast once in the server (or from x group)
## How the Bot Works
1) _**Need trigger to start**_ (this trigger will be in the form of someone typing in #scoreboard)
  * bot verifies if legit command 
    * correct syntax for ranking
    * check if decks exist in #decks for @player
      * if not webscrape for name using tappedout username, reverify, and reject if nothing new
  * anyone can type in scoreboard (bot asks a mod/admin for approval?)
2) _**#scoreboard Message manipulation**_ (i.e. ctrl c + ctrl v) 
  * bot copies message into local variable
  * bot deletes original message
  * bot enters message of variable info
3) _**Update #stats**_
  * delete every message in channel (except tappedout info for later use)
  * bot enters new data
    * rankings
    * any other statistics we want

## TODO:
- Finalize everything
- Program everything
- Add webhook in #game-dev-logs for this repo
