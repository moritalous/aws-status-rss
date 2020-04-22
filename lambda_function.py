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

output_soup = BeautifulSoup(rss_template, 'html.parser')


def get_rss_list():
    res = requests.get(base_url)
    aws_soup = BeautifulSoup(res.text, 'html.parser')

    links = [url.get('href')
             for url in aws_soup.find(id="AP_block").find_all('a')]
    links = list(set(links))
    links = list(filter(lambda x: x.startswith('/rss'), links))
    links = list(filter(lambda x: not('ap-southeast-1' in x), links))
    links = list(filter(lambda x: not('ap-southeast-2' in x), links))
    links = list(filter(lambda x: not('ap-south-1' in x), links))
    links = list(filter(lambda x: not('ap-northeast-2' in x), links))
    links = list(filter(lambda x: not('ap-northeast-3' in x), links))
    return links


def get_rss_item(rss_url):
    response = requests.get(rss_url)
    return response.text


def add_rss_item(rss_text):
    rss = BeautifulSoup(rss_text, 'html.parser')
    items = rss.find_all('item')
    for item in items:
        output_soup.find('channel').append(item)


def put_object(rss_string):
    import boto3

    client = boto3.client('s3')

    client.put_object(
        ACL='public-read',
        Body=rss_string.encode('utf-8'),
        Bucket=os.getenv('S3_BUCKET'),
        Key=os.getenv('S3_KEY')
    )


def lambda_handler(event, context):

    for rss in get_rss_list():
        text = get_rss_item(base_url + rss)
        add_rss_item(text)

    put_object(str(output_soup))
