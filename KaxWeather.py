from .. import loader, utils
import aiohttp

@loader.tds
class WeatherMod(loader.Module):
    """Модуль для просмотра погоды"""

    strings = {
        "name": "Kax:Weather",
        "no_city": "<emoji document_id=5319195671859841948>💙</emoji> <b>Укажите город</b>!",
        "error": "<emoji document_id=5319195671859841948>💙</emoji> <b>Ошибка получения погоды</b>.",
        "weather": "<emoji document_id=5318874640234330572>💙</emoji> <b>Погода в {}</b>\n\n"
        "<emoji document_id=5318830629704449481>💙</emoji> <b>Состояние: {}</b>\n"
        "<emoji document_id=5217541475365049478>🌟</emoji> <b>Температура: {}°C</b>\n"
        "<emoji document_id=5319031728663182464>💙</emoji> <b>Ветер: {} км/ч</b>\n"
        "<emoji document_id=5319112061731487637>💙</emoji> <b>Влажность: {}%</b>"
    }

    async def weathercmd(self, message):
        """Использование: .weather <город>"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["no_city"])
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://wttr.in/{args}?format=j1&lang=ru") as response:
                    if response.status != 200:
                        await utils.answer(message, self.strings["error"])
                        return
                    
                    weather_data = await response.json()
                    current = weather_data["current_condition"][0]
                    
                    await utils.answer(
                        message,
                        self.strings["weather"].format(
                            args,
                            current["lang_ru"][0]["value"],
                            current["temp_C"],
                            current["windspeedKmph"],
                            current["humidity"]
                        )
                    )
            except Exception:
                await utils.answer(message, self.strings["error"])