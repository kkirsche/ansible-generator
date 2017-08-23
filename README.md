# Ansible Generator

## Description
Ansible Generator is a python program designed to simplify creating a new
ansible playbook by creating the necessary directory structure for the user
based on ansible's best practices, as outlined in [content organization best practices](http://docs.ansible.com/ansible/latest/playbooks_best_practices.html#content-organization).

## Installation


### PIP
```
pip install -U ansible-generator
```

### Source

#### Without Make
```
git clone https://github.com/kkirsche/ansible-generator.git
cd ansible-generator
pip install -U wheel
python setup.py bdist_wheel --universal
pip install -U dist/*.whl
```
#### With Make
```
git clone https://github.com/kkirsche/ansible-generator.git
cd ansible-generator
make wheel
pip install -U dist/*.whl
```

## Usage

### Help Text

```
usage: ansible-generate [-h] [-a] [-v] [projects [projects ...]]

Generate an ansible playbook directory structure

positional arguments:
  projects

optional arguments:
  -h, --help            show this help message and exit
  -a, --alternate-layout
  -v, --verbose
```

### Example

Current directory:

```
ansible-generate
```

New-project:

```
ansible-generate playbook_name
```

Alternate Layout:

```
ansible-generate -a playbook_name
```

