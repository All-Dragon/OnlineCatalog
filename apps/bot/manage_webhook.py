import argparse
import asyncio
from urllib.parse import urlsplit, urlunsplit

from aiogram import Bot

from app.core.config import settings


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["set", "status", "delete"])
    parser.add_argument("--url")
    args = parser.parse_args()

    if args.action == "set":
        if args.url is None:
            mini_app_url = urlsplit(str(settings.mini_app_url))

            args.url = urlunsplit(
                (
                    mini_app_url.scheme,
                    mini_app_url.netloc,
                    "/telegram/webhook",
                    "",
                    "",
                ),
            )

        try:
            webhook_url = urlsplit(args.url)
        except ValueError:
            parser.error("Provide a valid HTTPS webhook URL")

        if webhook_url.scheme != "https" or not webhook_url.hostname:
            parser.error("Provide a valid HTTPS webhook URL")

    async with Bot(
        token=settings.telegram_bot_token.get_secret_value(),
    ) as bot:
        if args.action == "set":
            await bot.set_webhook(
                url=args.url,
                secret_token=(
                    settings.telegram_webhook_secret.get_secret_value()
                ),
                allowed_updates=["message"],
            )
            print("Webhook registered")

        elif args.action == "delete":
            await bot.delete_webhook(drop_pending_updates=False)
            print("Webhook removed")

        info = await bot.get_webhook_info()

        print("URL:", info.url or "(not registered)")
        print("Pending updates:", info.pending_update_count)
        print("Last error:", info.last_error_message or "(none)")


if __name__ == "__main__":
    asyncio.run(main())
