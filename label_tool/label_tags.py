import argparse
import os
import csv
from os import listdir
from os.path import isfile, join


def write_to_csv(values, file_name):
    with open(file_name, 'w+') as f:
        writer = csv.writer(f, delimiter=':')
        writer.writerow(['tag', 'label'])
        for key, value in values.items():
            writer.writerow([key, value])


def label_tags(tags, labels, labelled_tags, file_name):
    print("Enter label name or label index. ''Label'' is reserved name")

    try:
        for tag in tags:
            if tag in labelled_tags:
                continue
            if labels:
                print(labels)
            label = input("{}: ".format(tag))
            try:
                label = list(labels.keys())[list(labels.values()).index(int(label))]
            except ValueError:
                labels[label] = len(labels)
            labelled_tags[tag] = label

    except KeyboardInterrupt:
        pass

    write_to_csv(labelled_tags, file_name)


def get_all_tags(folder_path):
    os.chdir(folder_path)
    return [os.path.splitext(f)[0] for f in listdir(folder_path) if isfile(join(folder_path, f))]


def parse_existing_tags(tags_file):
    labels = dict()
    labelled_tags = dict()
    with open(tags_file, newline='') as f:
        reader = csv.reader(f, delimiter=':')
        for row in reader:
            if row[1] not in labels.keys():
                labels[row[1]] = len(labels)
            labelled_tags[row[0]] = row[1]

    return labels, labelled_tags


def main(args):
    all_tags = get_all_tags(args.path)
    if args.overwrite_tags:
        label_tags(all_tags, dict(), dict(), args.tags)
    else:
        labels, labelled_tags = parse_existing_tags(args.tags)
        label_tags(all_tags, labels, labelled_tags, args.tags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path to repository with data')
    parser.add_argument('--tags', help='CSV file with labelled tags')
    parser.add_argument('--overwrite_tags', default=False, action='store_true',
                        help='If true, then overwrite tags file. Otherwise, append.')

    main(parser.parse_args())
