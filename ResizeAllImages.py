import os
import os.path as osp

from PIL import Image


def main():
    base = '/home/larry/GitProjects/image-diff-viewer/output/'

    tag = 'res-comp-self'
    # base_path = osp.join(base, f'{tag}-res')
    # dest_path = osp.join(base, f'{tag}-resize')
    base_path = osp.join(base, f'{tag}')
    dest_path = osp.join(base, f'{tag}-resize')

    if not osp.exists(dest_path):
        os.mkdir(dest_path)

    for file in os.listdir(base_path):
        print(file)
        # if file.endswith('.png'):
        _img = Image.open(osp.join(base_path, file)).resize((600, 400))
        _img.save(osp.join(dest_path, file))


if __name__ == '__main__':
    # main()

    base_path = '/home/larry/GitProjects/image-diff-viewer/output/'

    file_name = '0123_GT-corp-black-edge'
    image = Image.open(osp.join(base_path, f'{file_name}.png')).resize((600, 400))
    image.save(osp.join(base_path, f'{file_name}-resize.png'))


