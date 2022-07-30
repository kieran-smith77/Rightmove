# Tinder For Rightmove (T4R)
This is a really really bad project, demonstrating how you could make a 'tinder for X' model application, in this case, for houses.

It uses a combination of a Rightmove Python package, some web scraping from the mobile app API and some Regex to parse info about the houses in your search which are then displayed in the website.

I made this because I hated going back to Rightmove and stumbling over the same rejects every time, this is not intended for use in any production environment. SERIOUSLY, DO NOT USE THIS!!


Reminder to get started:

```
git clone https://github.com/kieran-smith77/Rightmove.git
cd Rightmove
crontab -l | { cat; echo "0 9 * * * cd $(pwd)/scraper && ./main.py"; } | crontab -
docker run --rm -d -p 5000:5000 -v $(pwd)/db:/db  --name Rightmove $(docker build -q .)
```

Future ideas:
 - Add MFA
 - Support multiple users