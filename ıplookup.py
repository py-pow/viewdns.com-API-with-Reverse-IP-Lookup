import requests
from rich.console import Console
from rich import print
from rich.table import Table
from rich.prompt import Prompt
from bs4 import BeautifulSoup
import os
import argparse
from rich_argparse import RichHelpFormatter
import json
console = Console()

#https://api.viewdns.info/reverseip/?host=199.59.148.10&apikey=yourapikey&output=output_type
# 2fef61d0f8ee00037e225097a9439e1754f977b9


headers = {
    'Host': 'viewdns.info',
    'Cookie': '__utma=126298514.841522.1670842953.1670842953.1670842953.1; __utmb=126298514.4.10.1670842953; __utmz=126298514.1670842953.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __gads=ID=77eb26ab9f1d062f-22de459bfad90028:T=1670842953:RT=1670842953:S=ALNI_Ma4vZ_l-p7bSbdaoSCQac4boBiHdw; __gpi=UID=000008d016cb5d24:T=1670842953:RT=1670842953:S=ALNI_Ma-4UH8hoxt2sGddh_byCb1nirVHA; _fbp=fb.1.1670842953962.741475202; PHPSESSID=ga0v3u14pcihe7davpvo33nq42; __utmc=126298514',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    
}


pow = """
██████╗  ██████╗  ██████╗ ██╗    ██╗██╗    ██╗██╗    ██╗██╗██╗██╗
██╔══██╗██╔═══██╗██╔═══██╗██║    ██║██║    ██║██║    ██║██║██║██║
██████╔╝██║   ██║██║   ██║██║ █╗ ██║██║ █╗ ██║██║ █╗ ██║██║██║██║
██╔═══╝ ██║   ██║██║   ██║██║███╗██║██║███╗██║██║███╗██║╚═╝╚═╝╚═╝
██║     ╚██████╔╝╚██████╔╝╚███╔███╔╝╚███╔███╔╝╚███╔███╔╝██╗██╗██╗
╚═╝      ╚═════╝  ╚═════╝  ╚══╝╚══╝  ╚══╝╚══╝  ╚══╝╚══╝ ╚═╝╚═╝╚═╝
"""

poww = console.print(f"[blink red]{pow} [/] ", style="bold white on gray11") 
def argsFunc():

    
    ap = argparse.ArgumentParser(usage=poww,description="> Coded by  py_pow 'https://github.com/py-pow'",formatter_class=RichHelpFormatter)
    
    ap._optionals.title = f"Parametreler\n{'='*50}"
    
    ap.add_argument("-u", "--url", required=True,help="Used to enter domain / IP address.")
    ap.add_argument("-k", "--key", help="The API key is used to enter your value.")
    ap.add_argument("-o", "--output",default='txt',choices=['json','txt'],help="Used to specify the output format of the http response from the API.")
    #RichHelpFormatter.styles["argparse.url"] = "italic"
    
    args = ap.parse_args()

    #print("Girdiginiz sayi {} .".format(args["url"]))
    return args, ap
args, ap = argsFunc()
def keyLoad():
    global key,f
    
    
    
    path = r"key.txt"
    f = open(path, 'r+', encoding='utf-8')
    key = f.read() 
    if args.key == None and os.stat(path).st_size == 0:
        console.print(f"[blink]ERROR! [/] Key Not Found", style="bold red on gray11") 
        keyAsk = Prompt.ask("Would you like to add key information from this panel?", choices=["yes", "no"], default="yes")
        if keyAsk == 'yes':
             keyInput = console.input("Please enter your API key value: ")
             keyWrite = f.write(keyInput)
             key = f.read()
        elif keyAsk == 'no':
             console.print(f"[blink blue]INFORMATION! [/] Please add your key to the 'key.txt' file or use -k/--key", style="bold white on gray11") 
             exit()
        else:
            console.print(f"[blink]ERROR! [/]Invalid", style="bold red on gray11") 
            exit()
    elif args.key != None and os.stat(path).st_size == 0:
            keyWrite = f.write(args.key)
            console.log(f"[blink green]SUCCESS: [/] Key Added! ", style="bold green on gray11")
    else:
        console.log(f"[blink green]SUCCESS: [/] Key Found ", style="bold green on gray11")
    return key
          
def urlArgs():
    args.url = args.url.lower()
    if args.url.startswith('https'):
        args.url = args.url.replace('https://','')
        console.log(f"[blink red ]ERROR: [/]EXAMPLE: google.com ", style="bold green on gray11")
        exit()
        
    elif args.url.startswith('http'):
        args.url = args.url.replace('http://','')
        console.log(f"[blink red ]ERROR: [/]EXAMPLE: google.com ", style="bold green on gray11")
        exit()
        
    else:
        
        console.log(f"[blink green]SUCCESS: [/] Domain / IP accepted ", style="bold green on gray11")
        



   

def outputType():
    global site
    path = r"key.txt"
    f = open(path, 'r+', encoding='utf-8')
    key = f.read()
    print(key)
    args, ap = argsFunc()
    if args.output == 'json' or args.output == 'txt' or args.output == None:
         site = f"https://api.viewdns.info/reverseip/?host={args.url}&apikey={key}&output=json"
    else:
        print("Error")
    return site
    



    


def goLookup():
 args, ap = argsFunc()

 global listToStr
 r = requests.get(site).text

 if args.output == 'json' :
       rjson = BeautifulSoup(r, 'html.parser')
       if rjson.text == 'Query limit reached for the supplied API key.':
           console.print(f"[blink]ERROR! [/] Query limit reached for the supplied API key. You need a new API key", style="bold red on gray11") 
           exit()
       elif rjson.text == 'There was an error processing your API key - it may be invalid or disabled. Please try again later. If the problem continues to occur please contact the webmaster.':
           console.print(f"[blink]ERROR! [/]  API key Error", style="bold red on gray11") 
           exit()
       else:
           jsson = json.loads(str(rjson))
           intTo = int(jsson['response']['domain_count'])
           listjson = []
           x = 0
           while x < intTo:
            sa = jsson['response']['domains'][x]['name']
            listjson.append(sa)
            x += 1
     
            xjson = {
                  "Coded by 'py_pow' :  https://github.com/py-pow":'poowww!!!',
                  "Domain / IP you entered": "Domain : " + args.url,
                  "Total Domains Found ": jsson['response']['domain_count'],
                  "Domains ": listjson 
                  }
        
            with open(f"{args.url}.json", "w") as outfile:
             json.dump(xjson, outfile)
             outfile.close()
       console.print(f"[green]Domain: {args.url} [/]",justify="left")
       console.print(f"[cornflower_blue]{listjson} [/]",justify="left")
       console.print(f"[bold red]{x} Domains / IPs Found [/]",justify="left")
 elif args.output == 'txt' or args.output == None:
               
       jssona = BeautifulSoup(r, 'html.parser')
       
       if jssona.text == 'Query limit reached for the supplied API key.':
           console.print(f"[blink]ERROR! [/] Query limit reached for the supplied API key. You need a new API key", style="bold red on gray11") 
           exit()
       elif jssona == 'There was an error processing your API key - it may be invalid or disabled. Please try again later. If the problem continues to occur please contact the webmaster.':
           console.print(f"[blink]ERROR! [/]  API key Error", style="bold red on gray11") 
           exit()
       else:
        
          jssona = json.loads(str(jssona))
          intTo = int(jssona['response']['domain_count'])
         
          listjsontext = []
          t = 0
          while t < intTo:
            satext = jssona['response']['domains'][t]['name']
            listjsontext.append(satext)
            t += 1
            listToStr = ' '.join([str(elem) for elem in listjsontext])
            listToStr = listToStr.replace(' ','\n')
       console.print(f"[green]Domain: {args.url} [/]",justify="left")
       console.print(f"[cornflower_blue]{listToStr} [/]",justify="left")
       console.print(f"[bold red]{t} Domains / IPs Found [/]",justify="left")
            #console.print(" \n [bold red on gray11]poowww!!! : ",justify="left",style="")
            
    
       

       with open(f"{args.url}.txt", "w") as outfile:
          outfile.write(listToStr)
          outfile.close()  


     #rxml = BeautifulSoup(r, 'lxml')

      
        
    #console.log(f"Your Domain / IP => [bold green]{uriUser} [/]")

argsFunc()
urlArgs()
keyLoad()  
outputType()
goLookup()