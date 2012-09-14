#!/usr/bin/env python
# encoding: utf-8
'''
goo.gl extractor by John Milinovich
'''
import urllib, webbrowser, httplib, json, pprint

def GetToken():
  url = 'https://accounts.google.com/o/oauth2/auth?'
  encoded1 = urllib.urlencode({'response_type':'code',
                                'client_id':'{CLIENT ID HERE}',
                                'redirect_uri':'{REDIRECT URI HERE}',
                                'scope':'https://www.googleapis.com/auth/urlshortener',
                                'access_type':'offline',
                                'approval_prompt':'force'})
  send_url = '%s%s' % (url,encoded1)
  webbrowser.open_new(send_url)
  
  token = raw_input('spare a token, good sir: ')
  token_strip = token.strip()
  params = urllib.urlencode({'code':token_strip,
                                    'client_id':'{CLIENT ID HERE}',
                                    'client_secret':'{CLIENT SECRET HERE}',
                                    'redirect_uri':'{REDIRECT URI HERE}',
                                    'grant_type':'authorization_code'})
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  conn = httplib.HTTPSConnection('accounts.google.com')
  conn.request("POST","/o/oauth2/token",params,headers)
  response = conn.getresponse()
  
  print response.status, response.reason
  data = response.read()
  conn.close()  
  unpacked = json.loads(data.replace('\r\n', ''))
  return unpacked

def main():
  unpacked = GetToken()
  call_url='https://www.googleapis.com/urlshortener/v1/url/history?projection=FULL&access_token=%s&key={API KEY HERE}' % unpacked['access_token']
  a = urllib.urlopen(call_url).read()
  dict = json.loads(a)
  output_dict = {}
  tsv_file = open('shorty.tsv','w')
  for item in dict['items']:
    output_dict[item['id']]=[item['created'],item['analytics']['allTime']['shortUrlClicks'],item['longUrl']]
    line = '%s\t%s\t%s\t%s\r\n' % (item['id'],item['created'],item['analytics']['allTime']['shortUrlClicks'],item['longUrl'])
    tsv_file.write(line)
  tsv_file.close()
  
  
  
  #print dict['nextPageToken']
if __name__ == '__main__':
  main()
  
  
  