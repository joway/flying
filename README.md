# Flying

![PyPI](https://img.shields.io/pypi/v/flying.svg)

## Purpose

Make release easy again .

### Features
1. git tag
2. npm publish
3. docker build && push
4. pypi build && upload

## Example

[https://github.com/joway/flying-example](https://github.com/joway/flying-example)

## Install

```shell
pip install -U flying
```

## Usage

### init

Create `flying.json` template

```shell
flying init .
```

### release

Release current version which set in flying.json .

```shell
flying release
```

Automatically upgrade version (+0.0.1) 

```shell
flying release --upgrade
```

## Configuration

### Quick View

Template : `flying.json` 

```json
{
  "name": "flying-example",
  "version": "0.0.8",
  "version_prefix": "v",
  "conditions": [
    "git status | grep \"nothing to commit, working tree clean\""
  ],
  "pre_release": [
    "cat ./flying.json"
  ],
  "git": {
    "enable": true,
    "remote": "origin",
  },
  "docker": {
    "enable": true,
    "namespace": "joway/flying-example",
    "dkf_path": "./Dockerfile"
  },
  "npm": {
    "enable": true,
    "package_path": "./package.json"
  },
  "pypi": {
    "enable": false,
    "build_cmd": "python setup.py sdist",
    "upload_cmd": "twine upload dist/*"
  }
}
```

### version

`version_prefix + version` will be set as a tag for git and docker

### conditions

`conditions` is a shell commonds list , flying will check if every commond has a non-empty out . If not , it will exit without any release .

For Example , when you set :

```json
  "conditions": [
    "git status | grep \"nothing to commit, working tree clean\""
  ],
```

If your project has any un-commited file changes , it will be blocked .

### pre_release

`pre_release` is a shell commonds list , it will be exec before release jobs start .

For example , you can set this line if you are using webpack :

```json
"pre_release": ["npm run build"]
```

### git

Push new version tag to git remote server .

### docker

- `namespace`: For example , set it to 'joway/flying-example' , it will push docker image as `joway/flying-example:vx.x.x` (if version_prefix = "v") . 
- `dkf_path` : Dockerfile's path relative to the project root dir .

### npm

- `package_path`: package.json's path relative to the project root dir .

### pypi

Custom your own build && upload commond by set `build_cmd` and `upload_cmd`
