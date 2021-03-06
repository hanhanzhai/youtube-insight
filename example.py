#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Example to illustrate the usage of youtube_insight crawler.
"""

import sys, os, argparse, json, logging

from youtube_insight.crawler import Crawler


if __name__ == '__main__':
    # == == == == == == == == Part 1: Read video ids from file == == == == == == == == #
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file path of video ids or channel ids', required=True)
    parser.add_argument('-o', '--output', help='output file path of video data or channel video list', required=True)
    parser.add_argument('-c', '--channel', dest='channel', action='store_true', default=False)
    parser.add_argument('-f', '--force', dest='force', action='store_true', default=False)
    parser.add_argument('-r', '--relevant',  dest='relevant', action='store_true', default=False)
    parser.set_defaults(channel=False)
    parser.set_defaults(force=False)
    parser.set_defaults(relevant=False)
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    logging.basicConfig(filename='./youtube_crawler.log', level=logging.WARNING)

    if not os.path.exists(input_path):
        print('>>> Input file does not exist!')
        print('>>> Exit...')
        sys.exit(1)

    if os.path.exists(output_path) and not args.force:
        print('>>> Output file already exists, rename or backup it before starting new job!')
        print('>>> Exit...')
        sys.exit(1)

    output_data = open(output_path, 'w+')

    # == == == == == == == == Part 2: Set up crawler == == == == == == == == #
    d_key = 'Set your own developer key!'
    parts = 'snippet,contentDetails,statistics,topicDetails'
    fields = 'items(id,' \
             'snippet(publishedAt,channelId,title,description,thumbnails,channelTitle,categoryId,tags,defaultLanguage,defaultAudioLanguage),' \
             'contentDetails(duration,definition,caption,licensedContent,regionRestriction),' \
             'statistics,' \
             'topicDetails)'

    insight_crawler = Crawler()
    insight_crawler.set_key(d_key)
    insight_crawler.set_parts(parts)
    insight_crawler.set_fields(fields)

    # == == == == == == == == Part 3: Start crawler == == == == == == == == #
    # read the input file, start the crawler
    with open(input_path, 'r') as input_data:
        if args.channel:
            logging.info('>>> Crawling video ids for channels...')
            for cid in input_data:
                cid = cid.rstrip()
                channel_data = insight_crawler.crawl_channel_vids(cid)
                if channel_data is not None:
                    output_data.write('{0}\n'.format(json.dumps(channel_data)))
                    logging.info('--- Channel data crawler succeeded for channel: {0}'.format(cid))
                else:
                    logging.error('--- Channel data crawler failed for channel: {0}'.format(cid))
        else:
            logging.info('>>> Crawling insight data for videos...')
            for vid in input_data:
                vid = vid.rstrip()
                video_data = insight_crawler.crawl_insight_data(vid, args.relevant)
                if video_data is not None:
                    output_data.write('{0}\n'.format(json.dumps(video_data)))
                    logging.info('--- Insight data crawler succeeded for video {0}'.format(vid))
                else:
                    logging.error('--- Insight data crawler failed for video {0}'.format(vid))

    output_data.close()
