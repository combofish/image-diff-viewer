#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Combofish
# Filename: yaml_parser.py

import sys
import yaml


def get_yaml_data(yaml_file):
    data = yaml.load(open(yaml_file), Loader=yaml.FullLoader)
    return data


def config_parser(config_file_path='./config.yaml'):
    data = get_yaml_data(config_file_path)
    print(data)

    interval = data['interval']
    image_paths = data['image_paths']
    label_names = data['label_names']

    assert len(image_paths) == len(label_names), \
        "{image_paths} and {label_names} must have the same number."

    assert 1 <= len(image_paths) <= 12, \
        "{image_paths} have no more than 12 items."

    output_path = data['output_path']

    # print(interval, image_paths, label_names, output_path)
    return [interval, image_paths, label_names, output_path]


if __name__ == '__main__':
    config_parser()
