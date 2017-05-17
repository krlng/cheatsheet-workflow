# -*- coding: utf-8 -*-
import sys,requests, json
from workflow import Workflow, ICON_WEB, web
import re
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')

def getCheatSheets():
    host = 'http://35.157.154.191:9200'

    payload = {
       "query": {
            "query_string" : {
                "fields" : ["code^3","comment^2","file^2","content","section"],
                "query" : str(wf.args[0])
            }
        }
    }

    # json_data = json.dumps(data)
    cheatSheets = json.loads(requests.post(host+"/cheatsheets/markdown/_search", data=json.dumps(payload)).text)['hits']['hits']
    return cheatSheets

def parseElement(cmd):
    src = cmd['_source']
    item = {'title':"",'subtitle':"",'icon':"",'file':"",'link':"" }
    item["link"] = 'https://gitlab.com/kreiling/cheatsheets/blob/master/{}'.format(src['link'])
    item["id"] = cmd['_id']
    item["code"] = "invalid"
    item["title"] = "invalid"
    item["subtitle"] = "invalid"
    try:
        # if hasattr(src, 'comment'):
        if (src['tag']=='code' and str(src['info']).strip()=='sh'):
            item["code"] = src['code']
            item["title"]=src['code']
            item["subtitle"] = '{} ({})'.format(src['comment'],cmd['_score'])
        else:
            item["title"]=src['content']
            item["subtitle"] = '{} ({})'.format(src['file'],cmd['_score'])
            item["code"] = src['content']
    except Exception as e:
        item["code"] = "invalid code"
        item["title"] = "invalid entry"
        item["subtitle"] = src['content']

    item["icon"] = src['file'].split(".",1)[0]
    return item;

def main(wf):
    cheatSheets = getCheatSheets()
    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    for cmd in cheatSheets:
        try:
            item = parseElement(cmd)
            wf.add_item(
                title=item["title"],
                icon=u'imgs/{}.png'.format(item["icon"]),
                subtitle=item["subtitle"],
                # Pass multiple arguments, so that workflow can use the correct, depending on pressed keys
                # link => open GitLab Documentation
                # id => open ElasticSearch Document
                arg="{} {} {}".format(item["link"],item["id"], item["code"]),
                valid=True)


        # Send the results to Alfred as XML
        except Exception as e:
            link = 'http://35.157.154.191:9200/cheatsheets/markdown/_search?pretty&q=section:{}&q=content:{}&q=file:{}&default_operator=or'.format(wf.args[0],wf.args[0],wf.args[0])
            wf.add_item(title="Searched for:"+str(wf.args[0]),
                        subtitle="Exception Message: "+str(e),
                        arg="{} {} \"{}\"".format(link,"test", e),
                        valid=True)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow( update_settings={
        # Your username and the workflow's repo's name
        # 'github_slug': 'nik-ffm/inca-workflow',
        # Optional number of days between checks for updates
        # 'frequency': 1
    })
    # Install update if available
    # if wf.update_available:
    #     wf.start_update()
    sys.exit(wf.run(main))
