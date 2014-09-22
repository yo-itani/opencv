# -*- coding: utf-8 -*-

import requests
from xml.etree import ElementTree

"""
Compositeは使わなそうなので未対応

https://onedrive.live.com/view.aspx?resid=9C9479871FBFA822!109&app=Word&authkey=!ACvyZ_MNtngQyCU
"""
BING_API_BASE_URL = 'https://api.datamarket.azure.com/Bing/Search/'

IMAGE = 'Image'
VIDEO = 'Video'
NEWS = 'News'
SPELL = 'Spell'
RELATED_SEARCH = 'RelatedSearch'
JSON = 'json'
ATOM = 'atom'

def get(api_key, query, service='', format=JSON, top=50, skip=0, market=None, params=None):
    """ bing search apiから結果を取得する

        Args:
            api_key: apiキー
            query: 検索文字列(unicodeではなくutf8でエンコードされた文字列)
            service: 検索の種類(IMAGE, VIDEO, NEWS, SPELL, RELATED_SEARCH)
                     指定しなかった場合はweb検索
            format: レスポンスのフォーマット。json or atom(xml)
            top: 取得件数。最大は50
            skip: offset値。
            market: 対象地域。していなかった場合はIPアドレスなどから自動的に
                    選ばれる。
            params: その他追加で付加したいパラメータがあればディクショナリ
                    形式のパラメータを渡す
        Returns:
            dictionary(json) or elementtree(xml)
    """
    if not params:
        params = {}
    params['$format'] = format
    params['Query'] = "'%s'" % query
    params['$top'] = top
    params['$skip'] = skip
    if market:
        params['Market'] = market

    url = BING_API_BASE_URL + service
    response = requests.get(url, params=params, auth=('', api_key))
    if format == JSON:
        return response.json()
    else:
        return ElementTree.fromstring(response.content)


if __name__ == '__main__':
    pass
