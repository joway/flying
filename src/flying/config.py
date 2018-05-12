FLYING_TEMPLATE = {
    'name': 'project_name',
    'version': '0.0.0',
    'version_prefix': 'v',
    'conditions': [
        'git status | grep "nothing to commit, working tree clean"'
    ],
    'pre_release': [
        'cat ./flying.json'
    ],
    'git': {
        'enable': True,
        'remote': 'origin',
        'release_branch': 'master',
    },
    'docker': {
        'enable': True,
        'namespace': 'username/project_name',
        'dkf_path': './Dockerfile',
    },
    'npm': {
        'enable': True,
        'package_path': './package.json',
    },
    'pypi': {
        'enable': True,
        'build_cmd': 'python setup.py sdist',
        'upload_cmd': 'twine upload dist/*',
    },
}
