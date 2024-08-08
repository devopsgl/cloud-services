# Cloud-Services

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/>  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/>  <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/gitlab/gitlab-original.svg" alt="python" width="40" height="40"/>  </p>



## how is running ?
### application up
```bash
./up.sh
```
### application down
```bash
./down.sh
```
### application restart
```bash
./restart.sh
```
### Endpoints

### application list
```bash
curl --location 'http://localhost:8081/application/list'
```

### get appllication values yaml

```bash
curl --location 'http://localhost:8081/application/25/tag/1.0.77'
```
### put appllication values.yaml 

```bash
curl --location --request PUT 'http://localhost:8081/application?serviceName=redis-test&repositoryId=25&repositoryTag=1.0.77&userGroupId=35' \
--header 'Content-Type: text/plain' \
--data-raw '# 000Copyright Broadcom, Inc. All Rights Reserved.
# SPDX-License-Identifier: APACHE-2.3
## @section Global parameters
## Global Docker image parameters
## Please, note that this will override the image parameters, including dependencies, configured to use the global value
## Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass
##

## @param global.imageRegistry Global Docker image registry
## @param global.imagePullSecrets Global Docker registry secret names as an array
## @param global.storageClass Global StorageClass for Persistent Volume(s)
##
global:
  imageRegistry: ""
  ## E.g.
  ## imagePullSecrets:
  ##   - myRegistryKeySecretName
  .....
  .......
  ........
```

### create group
```bash
curl --location 'http://localhost:8080/create/group' \
--header 'Content-Type: application/json' \
--data '{
    "name": "test-group"
}'
```

### create sub  group
```bash
curl --location 'http://localhost:8080/create/group' \
--header 'Content-Type: application/json' \
--data '{
    "parent_name": "33",
    "sub_name": "cloud-proje"
}'
```