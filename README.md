## Railgen

Discord bot version of my Honkai: Star Rail showcase card maker, [Railcard](https://github.com/yuvlian/railcard).

It supports custom images.

WARNING: I have not implemented a limiter for the custom image file size (I don't need it). So if you're hosting it in a public server, beware that someone might do a funny and make you download one morbillion gigabytes.

To get started, run terminal as admin and type these in:

- `git clone https://github.com/yuvlian/railgen.git`
- `cd railgen`
- `pip install -r requirements.txt `

After that you can edit the token in main.py to your Discord bot token. 
Then just run this in the terminal: `python main.py`

Now you can start using the bot in Discord.

**Commands:**
- !help
  - This is self explanatory.
- !charlist [uid: int]
  - Gives you character list of the uid and the index number. Example usage: !uid 802775147
- !railgen [uid: int] [index: int] [image_url: str | none]
  - Generates the showcase card. If you put index 0, it will generate for all characters.
  - Example usages:
    - **!railgen 802775147 1 n** => this will generate card for the first character in !charlist without custom image
    - **!railgen 802775147 1** => this will generate card, but will ask first whether want to use custom image or not

**Example image:**

![image](https://github.com/yuvlian/railgen/assets/138542238/c684e928-7268-4de1-b4ab-406f04c1fb53)
