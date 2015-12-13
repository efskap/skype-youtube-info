import re
import pafy
import sys
import time
from imp import reload
sys.path.insert(0, './SkyPy')
from SkyPy import SkypeBot, SkypeMessageEvent, SkypeEditMessageEvent
import html


name = "youtube-sniffer"

ytpattern = re.compile("(?:http[s]?://www\.youtube\.com/watch\?v=|http[s]?://youtu.be/)([0-9A-Za-z\-_]*)(?:[#\?]t=([0-9]+))?")

YOUR_USER_NAME = ""
YOUR_PASSWORD = ""

class LinkSniffer(SkypeBot):
    def __init__(self, usern,passw):
        self.last_reply = None
        super().__init__(usern,passw,'tokenfile')
    prev = ''
    reply_pool = {}

    # finds youtube links in a message and generates info message strings
    def handleyt(self, msg):
        if name in msg.content or self.prev == msg.content:
            return
        yt_ids = list(set(ytpattern.findall(msg.content)))
        #print(str(msg.content.encode('utf-8')))
        if len(yt_ids) == 0:
            return
        for idd in yt_ids:
            print('Handling ' + idd[0])
            output=self.ytinfo(idd, '!nodesc' not in msg.content)
            #msg.chat.sendMsg(output, rich=True)
            self.prev=output
            yield output
    def remove_leading_zeroes(self,s,min_len=5):
        if len(s) > min_len and (s.startswith("0") or s.startswith(":")):
            return self.remove_leading_zeroes(s[1:])
        else:
            return s
    # gets youtube video's info and returns a formatted message string
    def ytinfo(self, tup, desc=True):
        id, secs = tup
        p = pafy.new(id)
        d = p.description.strip()
        if secs:
            s = self.remove_leading_zeroes(time.strftime('%H:%M:%S', time.gmtime(int(secs))))
            dur = s + "/" + self.remove_leading_zeroes(p.duration)
            id = id + "?t=" + secs
        else:
            dur = p.duration
        if len(d) > 300:
            d = d[0:300] + "..."
        return '<font size="13"><a href="https://www.youtube.com/watch?v='+ id + '">' + p.title + '</a></font><font  color="#5B6F73" size="13"> [' + dur + "]</font>" + "\n" +( ( '<font color="#5B6F73">' + d + "</font>") if desc else "")
    def onEvent(self, event):
        if isinstance(event, SkypeMessageEvent):
            #if (not event.msg.chat().has_attr('userIds') or len(event.msg.chat().userIds) < 5)
            href = ' <font size="7"><a href="https://github.com/efskap/skype-youtube-info">' + "(github)" + '</a></font>'
            header = '<font size="10" color="#6B523B">'+  name + '</font>' + href + "<br/>"
            separator = '<font color="#5B6F73"><br/><hr/></font>'
            replies = list(self.handleyt(event.msg))
            #print(str(event.msg.id) + " | " + str(event.msg.editId))
            if len(replies) > 0:
                output = header + separator.join(replies)
                if isinstance(event, SkypeEditMessageEvent) and self.last_reply is not None:
                    self.last_reply.edit(output,rich=True)
                else:
                    self.last_reply = event.msg.chat.sendMsg(output,rich=True)


            

            #this stuff is for formating my own messages, not really part of youtube-sniffer
            if event.msg.userId == self.userId and ('&lt;' in event.msg.content):# and '</font>' not in message.text:
                #m.edit('<font color="#00000" size="20">' + m.text + '</font>')
                t = event.msg.content
                t = t.replace("&apos;","'")
                t = t.replace('&lt;','<')
                t = t.replace('&gt;','>')
                t = t.replace('&quot;','"')
                t = t.replace('<i raw_pre="_" raw_post="_">.</i>','')
                print("editing to " + str(t.encode('utf-8')))
                event.msg.edit(t,rich=True)
                event.msg.edit(t,rich=True)

if __name__ == '__main__':
    while True:
        try:
            LinkSniffer(YOUR_USER_NAME, YOUR_PASSWORD)
        except Exception as e:
            print(str(e))
            pass




