from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client= Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Empty message')
        return
    valid_flag= user_message[0] == '>'
    if valid_flag:
        user_message = user_message[1:]
        try:
            response: str = get_response(user_message)
            await message.channel.send(response)
        except Exception as e:
            print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is running')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    if user_message[0:14] == '>load datacard':
        if len(message.attachments)==1:
            attachment= message.attachments[0]
            save_path = os.path.join('./', attachment.filename) #UPDATE DATACARD STORAGE DIRECTORY
            await attachment.save(save_path)
            await message.channel.send('Datacard saved')
        else:
            await message.channel.send('Corsika-Bot is only allowed to receive 1 datacard')

    else:
        await send_message(message, user_message)
                

def main() -> None:
    client.run(token=TOKEN)

if __name__=='__main__':
    main()

    
