import re
import pafy
import sys
from imp import reload
sys.path.insert(0, './SkyPy')
from SkyPy import SkypeBot, SkypeMessageEvent
import html


name = "youtube-sniffer"
ytpattern = re.compile("(?:http[s]?://www\.youtube\.com/watch\?v=|http://youtu.be/)([0-9A-Za-z\-_]*)")

YOUR_USER_NAME = ""
YOUR_PASSWORD = ""

class LinkSniffer(SkypeBot):
    def __init__(self, usern,passw):
        super().__init__(usern,passw,'tokenfile')
    prev = ''
    def handleyt(self, msg):
        if name in msg.content or self.prev == msg.content:
            return
        ids = list(set(ytpattern.findall(msg.content)))
        if len(ids) == 0:
            return
        for idd in ids:
            print('Handling ' + idd)
            output=self.ytinfo(idd, '!nodesc' not in msg.content)
            msg.chat.sendMsg(output, rich=True)
            self.prev=output
    def ytinfo(self, id, desc):
        p = pafy.new(id)
        d = p.description.strip()
        if len(d) > 300:
            d = d[0:300] + "..."
        href = ' <font size="7"><a href="https://github.com/efskap/skype-youtube-info">' + "(github)" + '</a></font>'
        return '<font size="10" color="#6B523B">'+  name + '</font>' + href + '\n<font size="13"><a href="https://www.youtube.com/watch?v='+ id + '">' + p.title + '</a></font><font  color="#5B6F73" size="13"> [' + p.duration + "]</font>" + "\n" +( ( '<font color="#5B6F73">' + d + "</font>") if desc else "")
    def onEvent(self, event):
        if isinstance(event, SkypeMessageEvent):
            #if (not event.msg.chat().has_attr('userIds') or len(event.msg.chat().userIds) < 5)
            self.handleyt(event.msg)


            #this stuff is for formating my own messages, not really part of youtube-sniffer
            if event.msg.userId == self.userId and ('&lt;' in event.msg.content):# and '</font>' not in message.text:
                #m.edit('<font color="#00000" size="20">' + m.text + '</font>')
                t = event.msg.content
                t = t.replace("&apos;","'")
                t = t.replace('&lt;','<')
                t = t.replace('&gt;','>')
                t = t.replace('&quot;','"')
                t = t.replace('<i raw_pre="_" raw_post="_">.</i>','')
                print("editing to " + t.encode('utf-8'))
                event.msg.edit(t,rich=True)
                event.msg.edit(t,rich=True)

if __name__ == '__main__':
    LinkSniffer(YOUR_USER_NAME, YOUR_PASSWORD)




