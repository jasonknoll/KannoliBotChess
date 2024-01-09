# Sawtooth - Chess Bot
### An attempt to learn how chess engines work
I've known about chess since I was a little kid, but up until recently I never played it. It's a fascinating game with limitless possibilities for creativity and strategy. 

I discovered the world of chess engines and chess bot competitions - I want to participate. Although machine learning will provide much more depth, Sawtooth uses **alpha-beta pruning** in a minmax search to find its moves. I'm using Python, which is arguably slower than other options, but it's easy for me to pickup and be productive with.

### Run the bot
First install the required packages in your desired Python environment with pip:
`pip install -r reqs.txt`

Then run Sawtooth in the command line by using: `python Sawtooth.py`

## TODO
- [ ] Connect to Lichess API
- [ ] Design and build Qt GUI
  - [ ] Add send/accept challenge functionality
  - [ ] Display current match data
  - [ ] Dispaly Lichess data (opponent name, ELO, etc.)
- [ ] Optimization
  - [ ] Move ordering
  - [ ] Probably many other things lmao 
