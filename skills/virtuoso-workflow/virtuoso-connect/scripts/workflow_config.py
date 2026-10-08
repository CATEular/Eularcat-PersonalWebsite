"""Read the suite's single private JSON config; never embed a user's paths."""
import argparse
import json
import os
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / 'config.local.json'

def load_config(path=None):
    source = Path(path or os.environ.get('VIRTUOSO_WORKFLOW_CONFIG') or DEFAULT_CONFIG).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError('Missing local workflow configuration: ' + str(source))
    config = json.loads(source.read_text(encoding='utf-8-sig'))
    if not isinstance(config, dict) or type(config.get('schema_version')) is not int or config['schema_version'] != 1:
        raise ValueError('Unsupported workflow configuration; schema_version must be 1')
    for group in ('local', 'bridge', 'remote', 'design', 'pdk'):
        if not isinstance(config.get(group), dict):
            raise ValueError('Configuration section must be an object: ' + group)
    return config

def require(config, key):
    value = config
    for part in key.split('.'):
        if not isinstance(value, dict) or part not in value:
            raise ValueError('Missing configuration field: ' + key)
        value = value[part]
    if value is None or value == '' or value == [] or value == {}:
        raise ValueError('Empty configuration field: ' + key)
    return value

def make_client(config=None, *, config_path=None, timeout=30):
    config = config if config is not None else load_config(config_path)
    # Explicit, process-scoped bridge config selection; the credential file stays untouched.
    from virtuoso_bridge.env import set_runtime_env_file, load_vb_env
    from virtuoso_bridge import VirtuosoClient
    env_file = Path(require(config, 'local.bridge_env_file')).expanduser()
    if not env_file.is_file():
        raise FileNotFoundError('Configured bridge .env file is missing')
    set_runtime_env_file(env_file)
    load_vb_env(env_file)
    profile = config.get('bridge', {}).get('profile')
    suffix = '_' + profile if profile else ''
    # Refuse a mismatched endpoint rather than silently connecting to another VM.
    for field, env_key in [('ssh_host','VB_REMOTE_HOST'),('ssh_user','VB_REMOTE_USER'),
                           ('local_port','VB_LOCAL_PORT'),('remote_port','VB_REMOTE_PORT')]:
        expected = config['bridge'].get(field)
        actual = os.environ.get(env_key + suffix)
        if expected not in (None, '') and str(expected) != actual:
            raise ValueError('Workflow configuration and bridge .env disagree on: bridge.' + field)
    return VirtuosoClient.from_env(timeout=timeout, profile=profile)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--key', help='Print one requested non-secret field, e.g. remote.executables.ocean')
    args = parser.parse_args()
    config = load_config(args.config)
    if args.key:
        if any(word in args.key.lower() for word in ('password','secret','token','private_key')):
            raise ValueError('Secret field output is unsupported')
        print(json.dumps(require(config, args.key), ensure_ascii=False))
    else:
        print('Workflow configuration loaded; environment fields are kept in config.local.json.')

if __name__ == '__main__':
    main()
