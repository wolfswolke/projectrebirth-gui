import yaml


def load_config():
    with open('config//gui_config.yaml', 'r') as f:
        config_file = yaml.safe_load(f)
    return config_file


def update_config_item(key, value, sub_key=None):
    with open('config//gui_config.yaml', 'r') as f:
        config_file = yaml.safe_load(f)
    if sub_key is None:
        config_file[key] = value
    else:
        config_file[key][sub_key] = value

