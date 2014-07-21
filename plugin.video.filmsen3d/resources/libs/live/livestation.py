import urllib,urllib2,re,cookielib,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
from resources.universal import watchhistory
    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def LivestationList(murl):
        main.GA("Live","Livestation")
        link=main.OPENURL('https://raw.github.com/mash2k3/MashUpStreams/master/livestation.xml')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<title>([^<]+)</title.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        for name,url,thumb in sorted(match):
            main.addPlayL(name,url,118,thumb,'','','','','',secName='Livestation News',secIcon=art+'/livestation.png')
                       
                       


def LivestationLink(mname,murl,thumb):
        link=main.OPENURL(murl)
        link=link.replace('href="/en/sessions/new','').replace('href="/en/contacts/new">','').replace('href="/redirect?locale=en">','')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match= re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        if len(match)>1:
            for url, name in match:
                main.addPlayL(mname+' '+name,'http://mobile.livestation.com'+url,118,thumb,'','','','','',secName='Livestation News',secIcon=art+'/livestation.png')
        else:
            LivestationLink2(mname,murl,thumb)
            
def LivestationLink2(mname,murl,thumb):
        main.GA("Livestation-"+mname,"Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Playing Link,1000)")
        stream_url =murl
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        infoL={'Title': mname, 'Genre': 'Live'} 
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='movie', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams='',imdb_id='')

        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]Livestation[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok
