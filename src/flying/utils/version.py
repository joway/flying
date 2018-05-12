def upgrade_version(cur_version):
    version_list = cur_version.split('.')
    big_version = version_list[0]
    mid_version = version_list[1]
    small_version = version_list[2]
    small_version = int(small_version) + 1

    return f'{big_version}.{mid_version}.{small_version}'
