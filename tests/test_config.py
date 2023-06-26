import os
import yaml
from ispdata import MODULE_DIR

def test_conf_keys():
    with open(os.path.join(MODULE_DIR, "config.yml"), 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    
    with open(os.path.join(MODULE_DIR, "config-example.yml"), 'r') as ymlfile:
        config_sample = yaml.safe_load(ymlfile)

    assert config.keys() ==  config_sample.keys()