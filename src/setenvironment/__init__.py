"""
setenvironment
"""

from .setenv import (
    Environment,
    add_env_path,
    add_template_path,
    get_env,
    get_env_var,
    get_paths,
    reload_environment,
    remove_env_path,
    remove_template_path,
    set_env_config_file,
    set_env_var,
    unset_env_var,
)

Environment = Environment
add_env_path = add_env_path
get_env_var = get_env_var
remove_env_path = remove_env_path
set_env_config_file = set_env_config_file
set_env_var = set_env_var
unset_env_var = unset_env_var
add_template_path = add_template_path
remove_template_path = remove_template_path
reload_environment = reload_environment
get_env = get_env
get_paths = get_paths
