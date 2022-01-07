# Tinder For Rightmove

To get started:

```
git clone https://github.com/kieran-smith77/Rightmove.git
cd Rightmove
crontab -l | { cat; echo "0 9 * * * cd $(pwd)/scraper && ./main.py"; } | crontab -
docker run --rm -d -p 5000:5000 -v $(pwd)/db:/db $(docker build -q .)
```
