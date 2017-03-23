import configparser

config_file = 'settings.conf'

config = configparser.ConfigParser()
config.read(config_file)

print(config)

for section in config:
    print(config[section])
    for setting in config[section]:
        print(setting, config[section][setting])
