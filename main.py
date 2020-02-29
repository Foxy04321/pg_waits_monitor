import config
import os.path
import warnings
import small_scale_plot
import PyQt5

conf_path = 'configurations.ini'

if not os.path.isfile(conf_path):
    warnings.warn('Process continiuse with default configurations!')
    current_config = config.create_default_config(conf_path)
else:
    current_config = config.get_config(conf_path)
small_scale_plot.show_plot(
    current_config['Generic settings']['host'],
    int(current_config['Generic settings']['port']),
    current_config['Generic settings']['dbname'],
    current_config['Generic settings']['user'],
    current_config['Generic settings']['password'],
    [wait.strip() for wait in current_config['Small scale plot settings']['wait_list'].split(',')]
)


