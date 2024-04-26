# GVE DevNet SDWAN Ansible Attach Device Template
This prototype leverages Ansible to attach device templates. The device information is derived from the database and formatted using Python. 
![/IMAGES/worflow.png](/IMAGES/workflow.png)

## Contacts
* Roaa AlKhalaf

## Solution Components
* Catalyst SDWAN
* Python
* Ansible
* SQLite DB
* vManage REST APIs



## Prerequisites
**Catalyst SD-WAN Credentials**: vManage REST API access control is based on sessions. All users will be able to get a session after successfully logging in. In order to use the Catalyst SD-WAN APIs, you need to make note of the vManage server IP address, username, and password of your instance of Catalyst SD-WAN. These credentials will be used to generate a session token and a CSRF prevention token if needed for POST operations. Note these values to add to the credentials file during the installation phase.

> For more information about Catalyst SD-WAN API authentication, read the [documentation](https://developer.cisco.com/docs/sdwan/#!authentication/how-to-authenticate)

## Installation/Configuration
1. Clone this repository with `git clone [repository name]`. To find the repository name, click the green `Code` button above the repository files. Then, the dropdown menu will show the https domain name. Click the copy button to the right of the domain name to get the value to replace [repository name] placeholder.
2. Add the required credentials and paths to the `.env` file:
```
VMA_HOST=vManage IP
VMA_USER=vManage username
VMA_PASSWORD=vManage password
MAPPINGS_PATH= path to the xlsx file that maps the DB values to the CSV values
PLAYBOOK_PATH=./code/playbooks/test.yml
DB_PATH=DB path
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

## Usage

# Python Scripts
There are 3 Python scripts in this repository: 
1. `create_mappings` script that reads the excel file that maps template to CSV. 
2. `get_devices` script that leverages the vManage REST APIs to retrieve the devices IDs to be used when attaching the device template. 
3. `main` script that handles the DB connection and retrieve the information for each device and attach and add it to the Ansible playbook. 

> Make sure to update the `map_templates_to_devices` dictionary. This is needed to determine the correct attachment of template to each device. 

To run the code, use the following command, note that the `test.yml` will be populated with devices information upon the successful execution of this main script:
```
$ python3 main.py
```
# Ansible 
1. Navigate to the `code` folder. 
2. Update the `inventory.yml` file:
```
all:
  hosts:
    vManage:
      ansible_host: vManage IP
      ansible_port: 443
      username: vManage username
      password: vManage password
```
3. Run the Ansible playbook with the following command:
```
$ ansible-playbook ./playbooks/test.yml
```

#
# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.