import os
import os.path as osp
import shutil

from yaml_parser import config_parser


def pick_out_images(image_paths, label_names, output_path):
    with open(osp.join(output_path, 'result.txt')) as f:
        names = f.readline()

    dest_path = osp.join(output_path, 'images')
    if not osp.exists(dest_path):
        os.mkdir(dest_path)

    for name in names.split(','):
        for idx, (_img_path, _label_name) in enumerate(zip(image_paths, label_names)):
            if idx == 0:
                src_img = osp.join(_img_path, f'{name}.jpg')
                dst_img = osp.join(dest_path, f'{name}_{_label_name}.jpg')
            else:
                src_img = osp.join(_img_path, f'{name}.png')
                dst_img = osp.join(dest_path, f'{name}_{_label_name}.png')

            print(f'Copying from "{src_img}" to "{dst_img}".')
            shutil.copy(src_img, dst_img)


if __name__ == '__main__':
    configs = config_parser(config_file_path='./config.yaml')

    interval, image_paths, label_names, output_path = configs
    pick_out_images(image_paths, label_names, output_path)
