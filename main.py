import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


TOKEN = '8047668775:AAFD3Gvnl5OtkxkjkbJK7mzjlmq4tqRJ-BcYOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = '@NewS_it_qwedfghnm_bot'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

URL = 'https://www.ixbt.com/news/'


latest_news = {}


async def fetch_html(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_latest_news():

    html = await fetch_html(URL)
    soup = BeautifulSoup(html, 'html.parser')

    news_list = []
    articles = soup.select('div[itemprop="itemListElement"]')

    for article in articles:
        title = article.select_one('a[itemprop="url"]').text.strip()
        link = article.select_one('a[itemprop="url"]')['href']
        full_link = f"https://www.ixbt.com{link}"

        if title not in latest_news:  # Если новость новая
            latest_news[title] = full_link  # Добавляем в словарь отслеживания
            news_list.append({'title': title, 'link': full_link})

    return news_list


async def send_news(news):

    for item in news:
        message = f"📰 {item['title']}\n{item['link']}"
        await bot.send_message(CHAT_ID, message)


async def news_checker():

    while True:
        latest_news_list = await get_latest_news()
        if latest_news_list:  # Если есть новые новости
            await send_news(latest_news_list)
        await asyncio.sleep(300)  # Проверяем сайт каждые 5 минут


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.reply("Бот для отслеживания новостей iXBT запущен! 📰")
    asyncio.create_task(news_checker())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
