import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from form import Ui_Form

import os.path as osp
import time

from yaml_parser import config_parser

debug_flag = False


def save_results(image_name_list, output_path):
    with open(osp.join(output_path, 'result.txt'), 'w') as f:
        f.write(','.join(image_name_list))


class WorkThread(QThread):
    trigger = pyqtSignal()

    def __init__(self, interval=1):
        super(WorkThread, self).__init__()
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            self.trigger.emit()


class QMyWidget(QWidget):
    def __init__(self, parent=None, paths=[], label_names=[], interval=1, output_path='./output/'):
        super(QMyWidget, self).__init__(parent)
        self.paths = paths

        # setup ui
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__init_exit_button()
        self.__init_string_labels(label_names=label_names)

        # selected list text
        # self.__ui.textEdit.moveCursor()
        self.selected_name_list = set()
        self.output_path = output_path
        if not osp.exists(self.output_path):
            os.mkdir(self.output_path)

        # init image names
        """
            self.image_names = sorted(image_names)
            self.image_numbers = len(self.image_names)
        """
        self.__init_image_names(paths=paths)

        # preparation Q-labels
        """
            self.img_labels = _Q_labels
        """
        self.__init_image_labels()

        # show first images
        self.index = 0
        self.show_images()

        self.auto_show_flag = False
        self.work = WorkThread(interval=interval)

        # functions of button
        self.__ui.previous_button.clicked.connect(self.show_previous)
        self.__ui.next_button.clicked.connect(self.show_next)
        self.__ui.auto_button.clicked.connect(self.auto_show)

        # radio button
        self.__ui.radioButton.setChecked(False)
        self.__ui.radioButton.toggled.connect(self.btn_state)

    def btn_state(self):
        btn = self.__ui.radioButton
        _name = self.image_names[self.index]
        if btn.isChecked():
            # print('btn selected')
            self.selected_name_list.add(_name)

            # save result
            save_results(self.selected_name_list, self.output_path)

        else:
            # print('btn is deselected')
            if _name in self.selected_name_list:
                self.selected_name_list.remove(_name)

        self.__ui.textEdit.setText(f'{",".join(self.selected_name_list)}')

    def auto_show(self):
        self.auto_show_flag = not self.auto_show_flag
        if self.auto_show_flag:
            self.work.start()
            self.work.trigger.connect(self.show_next)
            self.__ui.auto_button.setText('Stop')
        else:
            self.work.terminate()
            self.__ui.auto_button.setText('Auto')

    def show_next(self):
        index = self.index + 1
        if index >= self.image_numbers:
            index = 0

        self.index = index
        self.show_images()

    def show_previous(self):
        index = self.index - 1
        if index < 0:
            index = self.image_numbers - 1

        self.index = index
        self.show_images()

    def show_images(self):
        index = self.index

        # select
        if self.index in self.selected_name_list:
            self.__ui.radioButton.setChecked(True)
        else:
            self.__ui.radioButton.setChecked(False)

        # preparation
        img_name = self.image_names[index]
        images = load_images_by_name(self.paths, img_name)

        self.__ui.label_5.setText(f'{index}')
        self.__ui.label_4.setText(f'{img_name}')

        for _img, _lab in zip(images, self.img_labels):
            _lab.clear()
            _lab.setPixmap(_img)
            _lab.setScaledContents(True)

    def __init_exit_button(self):
        # exit button
        exit_btn = self.__ui.exit_button
        exit_btn.setShortcut('Ctrl+Q')
        exit_btn.clicked.connect(self.close)

    def __init_string_labels(self, label_names):
        # fixed string show
        self.__ui.label_1.setText("Image name:")
        self.__ui.label_2.setText("Current index:")
        self.__ui.label_3.setText("Total number:")

        # label string center, use label names
        string_labels = [
            self.__ui.label, self.__ui.label_7,
            self.__ui.label_8, self.__ui.label_9,
            self.__ui.label_10, self.__ui.label_11
        ]

        for _lab, _str in zip(string_labels, label_names):
            _lab.setAlignment(Qt.AlignCenter)
            _lab.setText(f'{_str}')

        # red
        string_labels[2].setStyleSheet('color: red')

    def __init_image_labels(self):
        positions = [(i, j) for i in range(2) for j in range(3)]
        _Q_labels = []
        for position in positions:
            _label = QLabel('----')
            _Q_labels.append(_label)
            self.__ui.gridLayout.addWidget(_label, *position)

        self.img_labels = _Q_labels

    def __init_image_names(self, paths):
        # ===== init images ===== #
        # read names from path
        image_names = [
            img_name.split('.')[0] for img_name in os.listdir(paths[0])
            if img_name.endswith('.jpg')
        ]

        # # read names from file
        # with open(osp.join(self.output_path, 'result_bak.txt')) as f:
        #     names = f.readline().strip()
        # image_names = set(names.split(','))

        # use
        self.image_names = sorted(image_names)
        print(self.image_names)
        print(len(self.image_names))
        self.image_numbers = len(self.image_names)

        # update text label
        self.__ui.label_6.setText(f'{self.image_numbers}')


def load_images_by_name(paths, name):
    """
    :param paths:
    :param name:
    :return:
    """
    assert len(paths) >= 1, "Error, empty paths..."
    outs_path = []
    for idx, img_path in enumerate(paths):
        if idx == 0:
            outs_path.append(osp.join(img_path, name + '.jpg'))
        else:
            outs_path.append(osp.join(img_path, name + '.png'))

    if debug_flag:
        print('\n'.join(outs_path))

    outs = [QPixmap(_path) for _path in outs_path]
    return outs


def main(interval, paths, label_names, output_path):
    app = QApplication(sys.argv)
    my_widget = QMyWidget(
        paths=paths,
        label_names=label_names,
        interval=interval,
        output_path=output_path
    )
    my_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    configs = config_parser(config_file_path='./config.yaml')
    # print(configs)
    main(*configs)
