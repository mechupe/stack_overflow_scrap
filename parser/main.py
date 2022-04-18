import os
import uuid
import argparse
from parses import parse_tags_page, parse_questions

# Directory to which output csv files will be generated
DATA_DIRECTORY = 'data_' + str(uuid.uuid4())


def write_to_csv_questions_for_tag(tag, directory, pages_to_parse):
    for x in range(1, pages_to_parse + 1):
        try:
            csv_export = parse_questions(x, current_tag=tag)
            csv_export.to_csv(f'{directory}/{tag}.csv', index=True, sep=':', mode='a')
        except:
            print("Page with tag {} and number {} failed to parse".format(tag, x))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions_pages', type=int, choices=range(0, 500), default=100,
                        help='Number of questions pages to parse. Every page contains 50 questions.')
    parser.add_argument('--tags_pages', type=int, choices=range(0, 10), default=1,
                        help='Number of tags pages to parse. Every page with tags contains 36 tags. '
                             'If tags list is not empty, then this value will be ignored.')
    parser.add_argument('--tags', '--names-list', nargs='+', default=[],
                        help='List of tags to parse. If empty, then all tags from first @ref tags_pages'
                             ' will be parsed.')

    args = parser.parse_args()

    data_directory = DATA_DIRECTORY
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    if not args.tags:
        for page in range(1, args.tags_pages + 1):
            print("Start parsing page {}/{} of tags".format(page, args.tags_pages))
            tags = parse_tags_page(page)

            for current_tag in tags:
                print("Start parsing {} tag".format(current_tag))
                write_to_csv_questions_for_tag(current_tag, data_directory, args.questions_pages)
    else:
        for current_tag in args.tags:
            print("Start parsing {} tag".format(current_tag))
            write_to_csv_questions_for_tag(current_tag, data_directory, args.questions_pages)

    print("Data generation is finished, check {} repository".format(data_directory))
