# -*- coding: utf-8 -*-
import sys,requests, json
from workflow import Workflow, ICON_WEB, web
import re
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')

def getEmployees():
    host = 'https://inca.inovex.de/_api'
    # payload = json.load(open("auth.json"))
    payload = {}
    try:
        payload['password'] = wf.get_password('inovex-inca-password')
    except PasswordNotFound:  # API key has not yet been set
        wf.send_feedback()
        return 0

    try:
        payload['username'] = wf.get_password('inovex-inca-username')
    except PasswordNotFound:  # API key has not yet been set
        wf.send_feedback()
        return 0

    payload['rememberMe'] = True
    
    # json_data = json.dumps(data)
    headers = {'Authorization':'Basic bmtyZWlsaW5nOkJlYXJpbmcuMTY=' ,'Origin':'https://inca.inovex.de' ,'Accept-Encoding':'gzip, deflate, br' ,'Accept-Language':'en-US,en;q=0.8,de;q=0.6' ,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' ,'Content-Type':'application/json;charset=UTF-8' ,'Accept':'application/json, text/plain, */*' ,'Referer':'https://inca.inovex.de/' ,'Cookie':'_ga=GA1.2.1211380720.1465820575' ,'Connection':'keep-alive'}
    req = requests.post(host+"/authenticate", data=json.dumps(payload), headers=headers)
    id_token = json.loads(req.text)['id_token']
    headers['Cookie'] = '_ga=GA1.2.1211380720.1465820575; X-INCA-AUTHORIZATION='+id_token
    empList = json.loads(requests.get(host+"/employee", headers=headers).text)
    return empList


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
        # print(emp['admission'][:7])
        pass
    except TypeError as e:
        elements.append("")  # emp tags
    return u' '.join(elements)

def search_by_skill(emp):
    """Generate a string search key for a emp"""
    elements = []
    return u' '.join(map(lambda x: x['name'],emp['skills']))


def main(wf):
    empList = wf.cached_data('empList', getEmployees, max_age=36000)

    regex = re.compile('[A-Za-z]+')


    # Get query from Alfred
    if len(wf.args):
        if (wf.args[0] == "new"):
            now = datetime.datetime.now()
            empList = wf.filter('{}-{:02d}'.format(str(now.year),now.month), empList, key=search_by_time)
        elif (wf.args[0] == "skill"):
            empList = wf.filter(wf.args[1], empList, key=search_by_skill)
        elif ( regex.match(wf.args[0]) ):
            empList = wf.filter(wf.args[0], empList, key=search_key_for_name,  min_score=20)
        else:
            empList = wf.filter(wf.args[0], empList, key=search_by_time,  min_score=20)
        # if (wf.args[0])
    else:
        query = None


    # If script was passed a query, use it to filter posts

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    for emp in empList:
        # try:
        #     location = emp['location']
        # except AttributeError:
        #     location = ''

        wf.add_item(title=emp['firstName']+' '+emp['lastName'],
                    icon=u'imgs/'+emp['userId']+'.jpg',
                    # icontype=u'fileicon',
                    subtitle='{} in {} | {}'.format(emp['lob'],emp['location'],emp['mobile']),
                    arg=emp['userId'],
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
