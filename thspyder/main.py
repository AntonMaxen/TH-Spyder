from thspyder.bot import Bot


def main():
    bot = Bot()
    bot.add_spiders_from_config("models/models.json")
    bot.load_spiders()
    bot.start()


if __name__ == '__main__':
    main()
