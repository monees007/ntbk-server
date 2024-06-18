import os


def to_camel_case(name):
    return ''.join(word.title() for word in name.split('_'))


def list_directories_in_camel_case(path):
    directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    return [to_camel_case(dir_name) for dir_name in directories]



def list_files_and_directories_in_camel_case(path):
    result = {}
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            result[to_camel_case(dir_name)] = []
        for file_name in files:
            parent_dir = to_camel_case(os.path.basename(root))
            relative_path = os.path.join(root.replace(path, ''), file_name)
            result[parent_dir].append((to_camel_case(os.path.splitext(file_name)[0]), relative_path))
    return result

print(list_files_and_directories_in_camel_case('assets'))

print(list_directories_in_camel_case('assets'))
