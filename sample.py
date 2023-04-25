import yaml

with open('config.yaml') as file:
    config = yaml.safe_load(file)

print(config)  # print the contents of the config dictionary
