"""Python binding for EasyRec REST API."""

import urllib
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import ElementTree

VIEWED_TOGETHER = "VIEWED_TOGETHER"
BOUGHT_TOGETHER = "BOUGHT_TOGETHER"
GOOD_RATED_TOGETHER = "GOOD_RATED_TOGETHER"


class EasyRec(object):

    def __init__(self, base_url, apikey, tenantid):
        self.base_url = base_url
        self.apikey = apikey
        self.tenantid = tenantid

    def signin(self, operatorId, password):
        args = ({
            'operatorId': operatorId,
            'password': password
        })
        url = self.base_url + 'operator/signin?' + urllib.urlencode(args)
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        token = root.find('token').text
        return token

    def view(self, userid, sessionid, itemid, itemdescription, itemurl,
            itemimageurl=None, actiontime=None, itemtype=None):
        # Set up the arguments for the REST call.
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'userid': userid,
            'sessionid': sessionid,
            'itemid': itemid,
            'itemdescription': itemdescription,
            'itemurl': itemurl
        })
        if itemimageurl is not None:
            args['itemimageurl'] = itemimageurl
        if actiontime is not None:
            args['actiontime'] = _datetime_to_str(actiontime)

        if itemtype is not None:
            args['itemtype'] = itemtype

        # Make the request and verify success.
        url = self.base_url + 'api/1.0/view?' + urllib.urlencode(args)
        s = urllib.urlopen(url).read()
        root = etree.fromstring(s)
        assert root.tag == 'easyrec'

    def buy(self, userid, sessionid, itemid, itemdescription, itemurl, 
            itemimageurl=None, actiontime=None):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'userid': userid,
            'sessionid': sessionid,
            'itemid': itemid,
            'itemdescription': itemdescription,
            'itemurl': itemurl,
        })
        if itemimageurl is not None:
            args['itemimageurl'] = itemimageurl
        if actiontime is not None:
            args['actiontime'] = _datetime_to_str(actiontime)
        url = self.base_url + 'api/1.0/buy?' + urllib.urlencode(args)
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'

    def rate(self, userid, sessionid, itemid, ratingvalue, itemdescription,
            itemurl, itemimageurl=None, actiontime=None):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'userid': userid,
            'sessionid': sessionid,
            'itemid': itemid,
            'ratingvalue': ratingvalue,
            'itemdescription': itemdescription,
            'itemurl': itemurl,
        })
        if itemimageurl is not None:
            args['itemimageurl'] = itemimageurl
        if actiontime is not None:
            args['actiontime'] = _datetime_to_str(actiontime)
        url = self.base_url + 'api/1.0/rate?' + urllib.urlencode(args)
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'

    def otherusersalsoviewed(self, itemid, userid=None):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'itemid': itemid
        })
        if userid is not None:
            args['userid'] = userid
        url = (self.base_url + 'api/1.0/otherusersalsoviewed?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            response.append(item)
        return response

    def otherusersalsobought(self, itemid, userid=None):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'itemid': itemid
        })
        if userid is not None:
            args['userid'] = userid
        url = (self.base_url + 'api/1.0/otherusersalsobought?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            response.append(item)
        return response

    def itemsratedgoodbyotherusers(self, itemid, userid=None):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'itemid': itemid
        })
        if userid is not None:
            args['userid'] = userid
        url = (self.base_url + 'api/1.0/itemsratedgoodbyotherusers?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            response.append(item)
        return response

    def recommendationsforuser(self, userid):
        """Retrieves recommendations for the user.

        Returns:
            a list of dictionaries mapping response item parameters to values
        """
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'userid': userid
        })
        url = (self.base_url + 'api/1.0/recommendationsforuser?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            response.append(item)
        return response

    def mostvieweditems(self, numberOfResults, timeRange):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'numberOfResults': numberOfResults,
            'timeRange': timeRange, 
        })
        url = (self.base_url + 'api/1.0/mostvieweditems?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            item['value'] = float(item_element.find('value').text)
            response.append(item)
        return response

    def mostboughtitems(self, numberOfResults, timeRange):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'numberOfResults': numberOfResults,
            'timeRange': timeRange, 
        })
        url = (self.base_url + 'api/1.0/mostboughtitems?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            item['value'] = float(item_element.find('value').text)
            response.append(item)
        return response

    def mostrateditems(self, numberOfResults, timeRange):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'numberOfResults': numberOfResults,
            'timeRange': timeRange, 
        })
        url = (self.base_url + 'api/1.0/mostrateditems?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            item['value'] = float(item_element.find('value').text)
            response.append(item)
        return response

    def bestrateditems(self, numberOfResults, timeRange):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'numberOfResults': numberOfResults,
            'timeRange': timeRange, 
        })
        url = (self.base_url + 'api/1.0/bestrateditems?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            item['value'] = float(item_element.find('value').text)
            response.append(item)
        return response

    def worstrateditems(self, numberOfResults, timeRange):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'numberOfResults': numberOfResults,
            'timeRange': timeRange, 
        })
        url = (self.base_url + 'api/1.0/worstrateditems?' + 
                urllib.urlencode(args))
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'
        recommended_items = root.find('recommendeditems')
        response = []
        for item_element in recommended_items.findall('item'):
            item = ({'id': item_element.find('id').text,
                'type': item_element.find('type').text,
                'description': item_element.find('description').text,
                'url': item_element.find('url').text.strip()
            })
            imageurl = item_element.find('imageurl').text
            if imageurl is not None and imageurl != '':
                item['imageurl'] = imageurl
            item['value'] = float(item_element.find('value').text)
            response.append(item)
        return response

    def importrule(self, security_token, itemfromid, itemtoid, assocvalue,
            assoctype):
        args = ({
            'token': security_token,
            'tenantid': self.tenantid,
            'itemfromid': itemfromid,
            'itemtoid': itemtoid,
            'assocvalue': assocvalue,
            'assoctype': assoctype
        })
        url = self.base_url + 'api/1.0/importrule?' + urllib.urlencode(args)
        root = ElementTree(file=urllib.urlopen(url)).getroot()
        assert root.tag == 'easyrec'

    def importitem(self, security_token, itemid, itemdescription, itemurl,
            itemimageurl=None):
        args = ({
            'token': security_token,
            'tenantid': self.tenantid,
            'itemid': itemid,
            'itemdescription': itemdescription,
            'itemurl': itemurl,
        })
        if itemimageurl is not None:
            args['itemimageurl'] = itemimageurl
        url = self.base_url + 'api/1.0/importitem?' + urllib.urlencode(args)
        resp = urllib.urlopen(url).read()

        root = etree.fromstring(resp)
        assert root.tag == 'easyrec'

    def setitemactive(self, itemid, active):
        args = ({
            'apikey': self.apikey,
            'tenantid': self.tenantid,
            'itemid': str(itemid),
            'active': str(active),
        })
        url = self.base_url + 'api/1.0/setitemactive?' + urllib.urlencode(args)

        resp = urllib.urlopen(url).read()

        root = etree.fromstring(resp)
        assert root.tag == 'easyrec'


def _datetime_to_str(datetime):
    return datetime.strftime("%d_%m_%Y_%H_%M_%S")
