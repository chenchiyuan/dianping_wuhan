# -*- coding: utf-8 -*-
import codecs
import fcntl

__author__ = 'chenchiyuan'

AREAS = [
    ('r6326', u'江滩'), ('r6324', u'解放公园正门'), ('r6325', u'武汉天地'), ('r6838', u'三阳广场'),
    ('r6336', u'黄鹤楼'), ('r6818', u'中南财大首义校区'), ('r6822', u'户部巷'), ('r6332', u'武昌火车站'),
    ('r6333', u'武汉大学'), ('r6334', u'洪山广场'), ('r6816', u'华中师范大学'), ('r6330', u'东湖景区  '),
    ('r6331', u'湖北省博物馆'), ('r6335', u'麦德龙岳家嘴店'), ('r6814', u'湖北大学'), ('r6827', u'徐东销品茂'),
    ('r6328', u'江汉路'), ('r6825', u'HAPPY站台'), ('r6826', u'新民众乐园'), ('r6835', u'港澳中心'),
    ('r6834', u'西北湖新世界'), ('r6327', u'汉口火车站'), ('r6836', u'菱角湖万达广场'), ('r6329', u'武广'),
    ('r6821', u'地质大学汉口校区'), ('r6824', u'K11'), ('r6828', u'庄胜崇光百货'), ('r6830', u'武汉国际广场'),
    ('r6837', u'世贸广场'), ('r6317', u'归元寺'), ('r6318', u'琴台大剧院'), ('r6319', u'汉阳站'),
    ('r6829', u'摩尔城'), ('r6831', u'湘隆时代广场'), ('r6812', u'理工大余家头校区'), ('r6320', u'华中科技大学'),
    ('r6321', u'鲁巷广场'), ('r6810', u'武汉科技学院'), ('r6815', u'中南民族大学'), ('r6817', u'中南财大南湖校区'),
    ('r6820', u'地质大学洪山校区'), ('r6832', u'光谷国际广场'), ('r6833', u'光谷步行街'), ('r6322', u'群光广场'),
    ('r6323', u'长江崇文广场'), ('r6811', u'理工大洪山'), ('r6813', u'江汉大学')
]

def smart_decode(item, start=0, end=0):
    if not item:
        return ''

    if isinstance(item, list):
        if start:
            return '__'.join(item[start, end])
        else:
            return '__'.join(item)

    else:
        return item

class Restaurant(object):
    def __init__(self, num, url, shop_name=None, tags=None, address=None, flavor=None, env=None,
                 service=None, trans=None, specials=None, recommendations=None,
                 recommendation_photos=None,shop_score=None, avg_price=None, collect=None, code=None):
        self.num = num
        self.url = smart_decode(url)
        self.shop_name = smart_decode(shop_name)
        self.tags = smart_decode(tags)
        self.address = smart_decode(address)
        self.flavor = smart_decode(flavor)
        self.env = smart_decode(env)
        self.service = smart_decode(service)
        self.trans = smart_decode(trans)
        self.specials = smart_decode(specials)
        self.recommendations = smart_decode(recommendations)
        self.recommendation_photos = smart_decode(recommendation_photos)
        self.shop_score = smart_decode(shop_score)
        self.avg_price = smart_decode(avg_price)
        self.collect = smart_decode(collect)
        if code:
            self.lat, self.lng = decode(code)
        else:
            self.lat = '0.0'
            self.lng = '0.0'

    def save(self):
        file = codecs.open("../../data/dianping_%s" %str(AREAS[int(self.num)][1]), 'a+', 'utf-8')
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(self.url+':::'+self.shop_name+':::'+self.lat+':::' + self.lng + ':::'
                   +self.tags+':::'+self.url+':::'+self.address+':::'+self.flavor+':::'
                   +self.env+':::'+self.service+':::'+self.trans+':::'+self.specials+':::'+self.recommendations+':::'
                   +self.recommendation_photos+':::'+self.shop_score+':::'+self.avg_price+':::'
                   +self.collect+':::'+'\n')
        fcntl.flock(file, fcntl.LOCK_UN)
        file.close()

#
#    @classmethod
#    def unlock(cls):
#        for count in range(len(AREAS)):
#            file = codecs.open("../../data/dianping_%s" %str(AREAS[count][1]), 'a+', 'utf-8')
#            fcntl.flock(file, fcntl.LOCK_UN)
#            file.close()


def to_base36(value):
    if not isinstance(value, int):
        raise TypeError("expected int, got %s: %r" % (value.__class__.__name__, value))

    if value == 0:
        return "0"

    if value < 0:
        sign = "-"
        value = -value
    else:
        sign = ""

    result = []

    while value:
        value, mod = divmod(value, 36)
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])

    return sign + "".join(reversed(result))

def decode(C):
    """解析大众点评POI参数
    """
    digi = 16
    add = 10
    plus = 7
    cha = 36
    I = -1
    H = 0
    B = ''
    J = len(C)
    G = ord(C[-1])
    C = C[:-1]
    J -= 1

    for E in range(J):
        D = int(C[E], cha) - add
        if D >= add:
            D = D - plus
        B += to_base36(D)
        if D > H:
            I = E
            H = D

    A = int(B[:I], digi)
    F = int(B[I+1:], digi)
    L = (A + F - int(G)) / 2
    K = float(F - L) / 100000
    L = float(L) / 100000
    return  str(K), str(L)
