import os
import requests
from bs4 import BeautifulSoup

base_url = 'https://status.aws.amazon.com'

rss_template = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<rss version="2.0">'
                '  <channel>'
                '    <title><![CDATA[AWS Service Status]]></title>'
                '    <link>http://status.aws.amazon.com/</link>'
                '    <description><![CDATA[AWS Service Status]]></description>'
                '  </channel>'
                '</rss>'
                )

def get_rss_list(block):
    print('start get_rss_list')
    res = requests.get(base_url)
    aws_soup = BeautifulSoup(res.text, 'lxml')
    
    # links = [url.get('href') for url in aws_soup.find(id="AP_block").find_all('a')]
    links = [url.get('href') for url in aws_soup.find(id=block).find_all('a')]
    links = list(set(links))
    links = list(filter(lambda x: x.startswith('/rss'), links))
    # links = list(filter(lambda x: not('ap-southeast-1' in x), links))
    # links = list(filter(lambda x: not('ap-southeast-2' in x), links))
    # links = list(filter(lambda x: not('ap-south-1' in x), links))
    # links = list(filter(lambda x: not('ap-northeast-2' in x), links))
    
    
    return links


def get_rss_item(rss_url):
    print(rss_url)
    response = requests.get(rss_url)
    return response.text


def add_rss_item(rss_text, rss_path, output_soup):
    rss = BeautifulSoup(rss_text, 'xml')
    items = rss.find_all('item')
    for item in items:
        item.description.append('[ from ' + rss_path + ']')
        output_soup.find('channel').append(item)


def put_object(rss_string, block):
    import boto3

    client = boto3.client('s3')

    client.put_object(
        ACL='public-read',
        Body=rss_string.encode('utf-8'),
        Bucket=os.getenv('S3_BUCKET'),
        Key='aws-status'+block+'.rss',
        ContentType='application/rss+xml'
    )


def lambda_handler(event, context):
    block = event['block']
    print(block)
    
    output_soup = BeautifulSoup(rss_template, 'xml')

    for rss in get_rss_list(block):
        text = get_rss_item(base_url + rss)
        add_rss_item(text, base_url + rss, output_soup)

    put_object(str(output_soup), block)
