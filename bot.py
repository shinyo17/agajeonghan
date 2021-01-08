import discord
import os
from selenium import webdriver
from discord.ext import commands, tasks

from random import choice

bot = commands.Bot(command_prefix='!')

status = ['재획', '사냥', '기보', '무토', '일퀘', '주간퀘', '수로']


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))

@bot.event
async def on_ready():
    change_status.start()
    print('Bot is online!')

@bot.command(name='ping', help='탁구를 해 봐요~')
async def ping(ctx):
    user = str(ctx.author).split('#')[0]
    await ctx.send(f'{user} 님! 받으세요~ pong!')

@bot.command(name='hello', help='아가정한이 인사해 줍니다!')
async def hello(ctx):
    user = str(ctx.author).split('#')[0]
    responses = [f'{user} 님! 안녕하세요!', f'{user} 님의 입장이 아주 나이스 했습니다!']
    await ctx.send(choice(responses))

@bot.command(name='bye', help='아가정한이 작별 인사를 합니다!')
async def bye(ctx):
    user = str(ctx.author).split('#')[0]
    responses = [f'{user} 님! 안녕히 가세요!', f'{user} 님! 다음에 또 만나요 우리 모두 슬퍼 말아요~']
    await ctx.send(choice(responses))

@bot.command(name='랭킹', help='캐릭터의 랭킹을 보여 줍니다!')
async def rank(ctx, *, content: str):
    nickname = str(content).split(' ')[0]
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(3)
    
    driver.get('https://maplestory.nexon.com/Ranking/World/Total')
    driver.find_element_by_name('search_text').send_keys(nickname)
    driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div/span[1]/span/a/img').click()
    
    you = driver.find_element_by_class_name("search_com_chk")
    td = you.find_elements_by_tag_name("td")
    rank = td[0].find_elements_by_tag_name("p")
    rank_num = rank[0]
    rank_num = rank_num.text
    job = td[1].find_element_by_tag_name("dl")
    rank_job = job.find_element_by_tag_name("dd")
    rank_job = rank_job.text
    level = td[2]
    rank_level = level.text.split(".")[1]
    pop = td[4]
    rank_pop = pop.text
    mapleguild = td[5]
    rank_guild = mapleguild.text

    driver.quit()

    aboutyou =f'''
    순위: {rank_num}
닉네임: {nickname}
레벨: {rank_level}
인기도: {rank_pop}
직업: {rank_job}
길드: {rank_guild}
    ''' 
    await ctx.send(aboutyou)

bot.run(os.environ['BOT_TOKEN'])

