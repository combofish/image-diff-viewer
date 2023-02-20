import argparse
import os
import os.path as osp
import shutil

from yaml_parser import config_parser


def main(interval, paths, label_names, output_path):
    with open('./output/result-bak-comp-self.txt') as f:
        names = f.readline().split(',')
        print(names)

        dest_path = './output/res-comp-self/'
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        for _str, path in zip(label_names, paths):
            print(path)
            for name in names:
                if osp.exists(osp.join(path, f'{name}.png')):
                    shutil.copy(
                        osp.join(path, f'{name}.png'),
                        osp.join(dest_path, f'{name}_{_str}.png')
                    )

                elif osp.exists(osp.join(path, f'{name}.jpg')):
                    shutil.copy(
                        osp.join(path, f'{name}.jpg'),
                        osp.join(dest_path, f'{name}_{_str}.jpg')
                    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    cfg = parser.parse_args()

    configs = config_parser(cfg.config)
    # print(configs)
    main(*configs)
