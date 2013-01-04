#  This file is part of Mylar.
#
#  Mylar is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Mylar is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Mylar.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import logger
import string
import urllib
import lib.feedparser
from bs4 import BeautifulSoup as Soup

def getComic(comicid,type):
    comicapi='583939a3df0a25fc4e8b7a29934a13078002dc27'
    #api
    PULLURL='http://api.comicvine.com/volume/' + str(comicid) + '/?api_key=' + str(comicapi) + '&format=xml&field_list=name,count_of_issues,start_year,last_issue,site_detail_url,image,publisher'

    #import library to do http requests:
    import urllib2

    #import easy to use xml parser called minidom:
    from xml.dom.minidom import parseString
    #all these imports are standard on most modern python implementations

    #download the file:
    #first we should check to see if file is in cache to save hits to api.
    #parsing error - will investigate later...
    cache_path='cache/'
    #if os.path.isfile( str(cache_path) + str(comicid) + '.xml' ) == 'True':
    #    pass
    #else:
    #    f = urllib2.urlopen(PULLURL)
    #    # write api retrieval to tmp file for caching
    #    local_file = open(str(cache_path) + str(comicid) + '.xml', 'wb')
    #    local_file.write(f.read())
    #    local_file.close
    #    f.close

    #file = open(str(cache_path) + str(comicid) + '.xml', 'rb')
 
    file = urllib2.urlopen(PULLURL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you downloaded
    dom = parseString(data)

    if type == 'comic': return GetComicInfo(comicid,dom)
    if type == 'issue': return GetIssuesInfo(comicid,dom)

def GetComicInfo(comicid,dom):

    #comicvine isn't as up-to-date with issue counts..
    #so this can get really buggered, really fast.
    tracks = dom.getElementsByTagName('issue')
    try:
        cntit = dom.getElementsByTagName('count_of_issues')[0].firstChild.wholeText
    except:
        cntit = len(tracks)
    trackcnt = len(tracks)
    # if the two don't match, use trackcnt as count_of_issues might be not upto-date for some reason
    if int(trackcnt) != int(cntit):
        cntit = trackcnt
        vari = "yes"
    else: vari = "no"
    #if str(trackcnt) != str(int(cntit)+2):
    #    cntit = int(cntit) + 1
    comic = {}
    comicchoice = []
    cntit = int(cntit)
    #retrieve the first xml tag (<tag>data</tag>)
    #that the parser finds with name tagName:
    comic['ComicName'] = dom.getElementsByTagName('name')[trackcnt].firstChild.wholeText
    comic['ComicName'] = comic['ComicName'].rstrip() 
    comic['ComicYear'] = dom.getElementsByTagName('start_year')[0].firstChild.wholeText
    comic['ComicURL'] = dom.getElementsByTagName('site_detail_url')[0].firstChild.wholeText
    if vari == "yes": 
        comic['ComicIssues'] = str(cntit)
    else:
        comic['ComicIssues'] = dom.getElementsByTagName('count_of_issues')[0].firstChild.wholeText
    comic['ComicImage'] = dom.getElementsByTagName('super_url')[0].firstChild.wholeText
    comic['ComicPublisher'] = dom.getElementsByTagName('name')[trackcnt+1].firstChild.wholeText

    comicchoice.append({
        'ComicName':              comic['ComicName'],
        'ComicYear':              comic['ComicYear'],
        'Comicid':                comicid,
        'ComicURL':               comic['ComicURL'],
        'ComicIssues':            comic['ComicIssues'],
        'ComicImage':             comic['ComicImage'],
        'ComicPublisher':         comic['ComicPublisher']
        })

    comic['comicchoice'] = comicchoice
    return comic

def GetIssuesInfo(comicid,dom):
    subtracks = dom.getElementsByTagName('issue')
    cntiss = dom.getElementsByTagName('count_of_issues')[0].firstChild.wholeText
    cntiss = int(cntiss)
    n = cntiss-1
    issue = {}
    issuechoice = []
    for subtrack in subtracks:
        if (dom.getElementsByTagName('name')[n].firstChild) is not None:
            issue['Issue_Name'] = dom.getElementsByTagName('name')[n].firstChild.wholeText
        else:
            issue['Issue_Name'] = 'None'
        issue['Issue_Number'] = dom.getElementsByTagName('issue_number')[n].firstChild.wholeText
        issue['Issue_ID'] = dom.getElementsByTagName('id')[n].firstChild.wholeText

        issuechoice.append({
             'Issue_ID':                issue['Issue_ID'],
             'Issue_Number':            issue['Issue_Number'],
             'Issue_Name':              issue['Issue_Name']
             })

        issue['issuechoice'] = issuechoice
        #logger.info(u"issue retrieval: " + issue['Issue_ID'] + "for Issue No." + issue['Issue_Number'])
        n-=1

    return issue

