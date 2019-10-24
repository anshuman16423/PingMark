import os
import pickle
import discord
import json
from requests import request
from bs4 import BeautifulSoup


commands = ['add_CC','add_CF','CC_rating','CF_rating','CF_code','CF_contest','help','CC_code']
def get_rank(rating):
    if rating<1200:
        return (0,'newbie')
    elif rating<1400:
        return (1,'pupil')
    elif rating<1600:
        return (2,'specialist')
    elif rating<1800:
        return (3,'expert')
    else:
        return (4,'candidate master')
def get_star(rating):
    if rating<1400:
        return 1
    elif rating<1600:
        return 2
    elif rating<1800:
        return 3
    elif rating<2000:
        return 4
    elif rating<2200:
        return 5
    elif rating<2500:
        return 6
    else:
        return 7
def getCC_user(user):
    profile=request('GET','https://www.codechef.com/users/'+user)
    print(profile)
    if not profile.ok:
        return False
    soup=BeautifulSoup(profile.content)
    rating = soup.find('div', attrs={'class':'rating-number'})
    #await message.channel.send('<h4>'+user+'<\h4>\n'+'Current rating: '+rating.text)
    return rating
def getCF_user(user):
    data = request('GET','https://codeforces.com/api/user.rating?handle='+user)
    if not data.ok:
        return ''
    data=data.json()
    ratings = data['result']
    return ratings[-1]['newRating']
    
def event_identifier(message):
    message_length=len(message)
    # matches string with [command_type]::[command attributes]:: ....
    check = message.split('::')
    if len(check)>=1:
        command = check[0]
        attr = check[1:]
        if command not in commands:
            return False
        return command,attr
    return False
def add_cc_handle(owner,handle):
    
    try:
        
        fin  = open('cc.dat','rb')
    except:
        fout = open('cc.dat','wb')
        fout.close()
        fin  = open('cc.dat','rb')
    while 1:
        try:
            user,username = pickle.load(fin)
            if user==owner or username==handle :
                fin.close()
                return False
        except:
            fin.close()
            break
    fout = open('cc.dat','ab')
    pickle.dump((owner,handle),fout)
    fout.close()
    return True
def add_cf_handle(owner,handle):
    try:
        
        fin  = open('cf.dat','rb')
    except:
        fout = open('cf.dat','wb')
        fout.close()
        fin  = open('cf.dat','rb')
    while 1:
        try:
            user,username = pickle.load(fin)
            if user==owner or username==handle:
                fin.close()
                return False
        except:
            fin.close()
            break
    fout = open('cf.dat','ab')
    pickle.dump((owner,handle),fout)
    
    fout.close()
    return True


def cf_ranklist(contest_code):
    fin = open('cf.dat','rb')
    guild_handles = {}
    while 1:
        try:
            user,username = pickle.load(fin)
            guild_handles[username] = user
        except:
            fin.close()
            break
    url = "https://codeforces.com/api/contest.ratingChanges?contestId="+str(contest_code)
    page = request('GET',url)
    if not page.ok:
        return []
    data = page.json()
    ranklist = []
    counter = 1
    for row in data['result']:
        username = row['handle']     # works for non team handles else only first handle considered
        if guild_handles.get(username,None):
            ranklist.append((counter,row['rank'],username,guild_handles[username],row['oldRating'],row['newRating']))
            counter += 1
    return ranklist 
    
fin=open('token.txt','r')
token=fin.readline().strip()
fin.close()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content
    content=content.strip()
    if content[0]=='>':
        content=content[1:]
    else:
        return
        
    if not message.guild:
        await message.channel.send("no replies to DM's  :punch:")
        return
    if event_identifier(content):
        command,attr=event_identifier(content)
        print('command')
        if command=='add_CC':
            user=attr[0]
            profile=request('GET','https://www.codechef.com/users/'+user)
            print(profile)
            if not profile.ok:
                await message.channel.send('Invalid codechef username or try after some time')
                return
            try:
                
                if add_cc_handle(str(message.author),attr[0]):
                    soup=BeautifulSoup(profile.content)
                    rating = soup.find('div', attrs={'class':'rating-number'})
                    await message.channel.send('Current user rating: '+rating.text)
                    await message.channel.send('username added success')
                else:
                    await message.channel.send('owner or user alerady exist')
            except IndexError:
                await message.channel.send('Improper Command')
    
        elif command=='add_CF':
            try:
                if add_cf_handle(str(message.author),attr[0]):
                    data = request('GET','https://codeforces.com/api/user.rating?handle='+attr[0])
                    if not data.ok:
                        await message.channel.send('Invalid codeforces handle')
                        return
                    data=data.json()
                    ratings = data['result']
                    rank = get_rank(ratings[-1]['newRating'])
                    user=message.author
                    # Issue#1 adding roles error 403
                    #await user.add_roles(discord.utils.get(user.guild.roles, name=rank[1]))
                    await message.channel.send('Database Updated\n>'+attr[0]+":"+rank[1]+"("+str(ratings[-1]['newRating'])+")")
                else:
                    await message.channel.send('owner or user alerady exist')
            except IndexError:
                await message.channel.send('Improper Command')
        elif command=='CC_rating':
            user=attr[0]
            rating = getCC_user(user)
            if not rating:
                await message.channel.send('Invalid User\n try again after sometime')
            else:
                rank=get_star(int(rating.text))
                stars=':star: '*rank
                stars+='\n'
                await message.channel.send('**'+user+'**\n'+stars+'Current rating: '+rating.text)
        elif command=='CF_rating':
            user = attr[0]
            if user=='all':
                fin1 =open('cf.dat','rb')
                all_users = []
                c=0
                while 1:
                    try:
                        owner, user = pickle.load(fin1)
                        print(owner,user)
                        rating = getCF_user(user)
                        all_users.append((rating, user, owner))
                    except EOFError:
                        break
                    
                fin1.close()
                all_users.sort(reverse=True)
                result='```'
                print(len(all_users))
                c=1
                for user in all_users:
                    result+=str(c)+"    "+str(user[0])+"     "+user[1]+(" "*(15-len(user[1])))+user[2]+'\n'
                    c+=1
                await message.channel.send(result+'```')
                return
            rating = getCF_user(user)
            
            if not rating:
                await message.channel.send('Invalid User :grimacing:')
                return
            await message.channel.send('**'+user+'**\n'+"Current User Rating: "+str(rating))
        elif command=='CF_code':
            if len(attr)!=2:
                await message.channel.send('poorly structured command')
                return
            contest_code = attr[0]
            submission_code = attr[1]
            url = 'https://codeforces.com/contest/'+contest_code+'/submission/'+submission_code
            source = request('GET',url)
            if not source.ok or not source.content:
                await message.channel.send('check contest code and submission code')
                return
            print(source)
            soup = BeautifulSoup(source.content)
            code = '```cpp\n'
            
            content = soup.find('pre',attrs={'id':'program-source-text'})
            if not content:
                await message.channel.send('check your contest code')
                return
            for i in content:
                code+=i
            code+="```"
            length = len(code)
            if length>2000:
                i=0
                code = code[7:]
                code = code[:-3]
                while i<length:
                    code_new=code[i:i+1900]
                    await message.channel.send("```cpp\n"+code_new+"```")
                    i+=1900
                return
            await message.channel.send(code)
            return
        elif command == 'CF_contest':
            if len(attr)!=1:
                await message.channel.send('poorly structured command')
                return
            contest_code = attr[0]
            ranklist = cf_ranklist(contest_code)
            if not ranklist:
                await message.channel.send('No Paricipation :punch:')
                return
            final_ranklist = "```SERVER CONTEST RANKLIST "+str(contest_code)+'\n'
            for row in ranklist:
                final_ranklist += "       ".join(map(str,row[:-3]))
                spaces = 20-len(row[-4])
                final_ranklist += " "*spaces + row[-3][:20]
                final_ranklist += " "*(23-min(20,len(row[-3])))+("+"+str(row[-1]-row[-2]) if row[-1]>row[-2] else str(row[-1]-row[-2]))
                final_ranklist += '\n'
            final_ranklist += '```'
            await message.channel.send(final_ranklist)
            return
        elif command == 'CC_code':
            if len(attr)!=1:
                await message.channel.send('Invalid command structure')
                return
            url = "https://www.codechef.com/viewsolution/"+str(attr[0])
            page = request('GET',url, headers={'User-Agent': 'Mozilla/5.0'})
            if not page.ok:
                await message.channel.send('Invalid code!!!')
                return
            soup = BeautifulSoup(page.content)
            content = soup.find_all('script')
            data=''
            for block in content:
                if 'meta_info' in block.text:
                    data=block.text
                    break
            if not data:
                await message.channel.send('Something went wrong!!')
                return
            data = data[data.find('{'):-2]
            data = json.loads(data)
            code="```cpp\n"
            code+=data['data']['plaintext']
            code+="```"
            length = len(code)
            if length>2000:
                i=0
                code = code[7:]
                code = code[:-3]
                while i<length:
                    code_new=code[i:i+1900]
                    await message.channel.send("```cpp\n"+code_new+"```")
                    i+=1900
                return
            await message.channel.send(code)
            return
        elif command == 'help':
            await message.channel.send("List commands that can be used")
            # TODO
            message_str="\n".join(commands)
            message_str+='\n'
            message_str+="For more details or contributing visit https://github.com/anshuman16423/PingMark"
            await message.channel.send(message_str)
        
            
        
           
            
            
client.run(token)

