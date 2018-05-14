import os

import fire

from flying.config import FLYING_TEMPLATE, FLYING_DEFAULT
from flying.utils.cmd import run_cmd
from flying.utils.io import write_json_into_file, read_json_from_file, merge_json
from flying.utils.version import upgrade_version

COMMIT_TYPE_FLAGS = {
    "feature": "✨feature",
    "bugfix": "🐛bugfix",
    "hotfix": "🚑hotfix",
    "docs": "📚docs",
    "style": "🎨style",
    "refactor": "🏗️refactor",
    "test": "✅test",
    "chore": "🔨chore",
    "release": "🎉release",
    "text": "📝text",
    "addlog": "🔉add log",
    "dellog": "🔇delete log",
}
COMMIT_TYPE_CHOICE = COMMIT_TYPE_FLAGS.keys()


def log_info(msg):
    print(msg)


def log_error(msg):
    print(msg)


def git_tag_and_push(tag, remote):
    tag_cmd = f'git tag {tag}'
    success, stdout = run_cmd(tag_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)

    push_cmd = f'git push {remote} {tag}'
    success, stdout = run_cmd(push_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)
    return True


def docker_build_and_push(namespace, tag, dkf_path):
    image_tag = f'{namespace}:{tag}'
    build_cmd = f'docker build -f {dkf_path} -t {image_tag} .'
    success, stdout = run_cmd(build_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)

    push_cmd = f'docker push {image_tag}'
    success, stdout = run_cmd(push_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)
    return True


def npm_upgrade_and_publish(tag, package_path, upgrade_version_enable=False):
    package = read_json_from_file(package_path)
    package['version'] = tag
    if upgrade_version_enable:
        write_json_into_file(package_path, package)

    publish_cmd = 'npm publish'
    success, stdout = run_cmd(publish_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)
    return True


def pypi_build_and_upload(build_cmd, upload_cmd):
    success, stdout = run_cmd(build_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)

    success, stdout = run_cmd(upload_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)
    return True


def git_commit(commit_type, commit_msg):
    message = f'[{COMMIT_TYPE_FLAGS[commit_type]}]: {commit_msg}'
    cmt_cmd = f'git commit -m "{message}"'
    success, stdout = run_cmd(cmt_cmd)
    if not success:
        log_error(stdout)
        return False
    log_info(stdout)
    return True


class Flying(object):
    @staticmethod
    def init(directory=os.getcwd()):
        path = os.path.abspath(directory)
        write_json_into_file(f'{path}/flying.json', FLYING_TEMPLATE)

    @staticmethod
    def release(directory=os.getcwd(), upgrade=False):
        path = os.path.abspath(directory)
        flying_path = f'{path}/flying.json'
        flying_config = read_json_from_file(flying_path)
        flying_config = merge_json(flying_config, FLYING_DEFAULT)

        name = flying_config['name']
        version = flying_config['version']
        version_prefix = flying_config['version_prefix']
        git = flying_config['git']
        docker = flying_config['docker']
        npm = flying_config['npm']
        pypi = flying_config['pypi']
        pre_release = flying_config['pre_release']
        conditions = flying_config['conditions']

        if upgrade:
            version = upgrade_version(version)
            flying_config['version'] = version
        tag = version_prefix + version

        # any condition should stdout at least one character to make sure that
        # the project is ready for release
        for condition in conditions:
            success, out = run_cmd(condition)
            if out == '':
                log_error(f'Can not satisfy the condition: \n  {condition}')
                return
            if not success:
                log_error(out)
                return
            log_info(out)

        for pre_cmd in pre_release:
            success, out = run_cmd(pre_cmd)
            if not success:
                log_error(out)
                return
            log_info(out)

        if git['enable']:
            log_info('triggered git release')
            success = git_tag_and_push(
                tag=tag,
                remote=git['remote'],
            )
            if not success:
                log_info('git release failed')
            else:
                log_info('git release success')
        if docker['enable']:
            log_info('triggered docker release')
            success = docker_build_and_push(
                namespace=docker['namespace'],
                tag=tag,
                dkf_path=docker['dkf_path'],
            )
            if not success:
                log_info('docker release failed')
            else:
                log_info('docker release success')
        if npm['enable']:
            success = npm_upgrade_and_publish(
                tag=tag,
                package_path=npm['package_path'],
                upgrade_version_enable=npm['upgrade_version_enable'],
            )
            if not success:
                log_info('npm release failed')
            else:
                log_info('npm release success')
        if pypi['enable']:
            success = pypi_build_and_upload(
                build_cmd=pypi['build_cmd'],
                upload_cmd=pypi['upload_cmd'],
            )
            if not success:
                log_info('pypi release failed')
            else:
                log_info('pypi release success')

        write_json_into_file(flying_path, flying_config)
        if upgrade:
            return f'upgraded and released project {name}'
        return f'released project {name}'

    @staticmethod
    def commit(commit_type, commit_msg):
        if commit_type not in COMMIT_TYPE_CHOICE:
            return f'commit type : {commit_type} is not included in \n{", ".join(COMMIT_TYPE_CHOICE)}'
        success = git_commit(commit_type, commit_msg)
        if not success:
            log_info('git commit failed')
        else:
            log_info('git commit success')


def main():
    try:
        fire.Fire(Flying)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log_error(e)


if __name__ == '__main__':
    main()
