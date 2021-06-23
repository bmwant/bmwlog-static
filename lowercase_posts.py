import os
import shutil


def lowercase_filenames():
    dir_path = 'source/_posts'
    for filename in os.listdir(dir_path):
        old_filepath = os.path.join(dir_path, filename)
        new_filepath = f'{os.path.join(dir_path, filename.lower())}-1'
        print(new_filepath)
        shutil.move(old_filepath, new_filepath)


if __name__ == '__main__':
    lowercase_filenames()
