"""Python binding for EasyRec REST API."""

from xml.etree.ElementTree import ElementTree
from xml.etree import ElementTree as etree
import urllib

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
            itemimageurl=None, actiontime=None):
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

        # Make the request and verify success.
        url = self.base_url + 'api/1.0/view?' + urllib.urlencode(args)
        #root = ElementTree(file=urllib.urlopen(url)).getroot()
        s = urllib.urlopen(url).read()
        print args,repr(s)
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

        #root = ElementTree(file=).getroot()
        root = etree.fromstring(resp)#.getroot()
        assert root.tag == 'easyrec'

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

def _datetime_to_str(datetime):
    return datetime.strftime("%d_%m_%Y_%H_%M_%S")
    
