# -*- coding: utf-8 -*-
import sys,requests, json
from workflow import Workflow, ICON_WEB, web
import re
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')


def search_key_for_name(emp):
    """Generate a string search key for a emp"""
    elements = []
    elements.append(emp['firstName'])  # emp tags
    elements.append(emp['lastName'])  # title of emp
    try:
        elements.append(emp['location'])  # location of emp
        pass
    except TypeError as e:
        elements.append("")  # emp tags
    try:
        elements.append(emp['lob'])  # lob of emp
        pass
    except TypeError as e:
        elements.append("")  # emp tags

    return u' '.join(str(elements))


def search_by_time(emp):
    """Generate a string search key for a emp"""
    elements = []
    try:
        elements.append(str(emp['admission'][:7]))  # emp tags
        pass
    except TypeError as e:
        elements.append("")  # emp tags
    return u' '.join(elements)

def search_by_skill(emp):
    """Generate a string search key for a emp"""
    elements = []
    return u' '.join(map(lambda x: x['name'],emp['skills']))


def main(wf):

    def getCheatSheets():
        host = 'http://35.157.154.191:9200'

        payload = {
           "query": {
                "query_string" : {
                    "fields" : ["file","content","section"],
                    "query" : str(wf.args[0])
                }
            }
        }

        # json_data = json.dumps(data)
        cheatSheets = json.loads(requests.post(host+"/cheatsheets/markdown/_search", data=json.dumps(payload)).text)['hits']['hits']
        return cheatSheets

    cheatSheets = getCheatSheets()
    # print("type", file=sys.stderr)
    # wf.logger.debug(type(cheatSheets))

    regex = re.compile('[A-Za-z]+')
    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    for cmd in cheatSheets:
        src = cmd['_source']
        link = 'https://gitlab.com/kreiling/cheatsheets/blob/master/{}'.format(src['link'])
        id = cmd['_id']
        if hasattr(src, 'comment'):
            subtitle = '{} ({})'.format(src['comment'],cmd['_score'])
        else:
            subtitle = '{} ({})'.format(src['file'],cmd['_score'])
        wf.add_item(title=src['content'],
                    # icontype=u'fileicon',
                    icon=u'imgs/{}.png'.format(src['file'].split(".",1)[0]),
                    subtitle=subtitle,
                    # arg=src['link'],
                    arg="{} {}".format(link,id),
                    valid=True)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow( update_settings={
        # Your username and the workflow's repo's name
        'github_slug': 'nik-ffm/inca-workflow',
        # Optional number of days between checks for updates
        'frequency': 1
    })
    # Install update if available
    if wf.update_available:
        wf.start_update()
    sys.exit(wf.run(main))
