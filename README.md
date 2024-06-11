# easy_allure

Package to facilitate work with allure testops

## Installation

```shell
pip3 install easy-allure
```
To work with easy_allure, ENV variables for testops should be set in your working environment
```shell
export ALLURE_ENDPOINT=ENDPOINT_HERE
export ALLURE_TOKEN=TOKEN_HERE
export ALLURE_PROJECT_ID=ID_HERE
```

For updating MR description with last Testops launch link (only Gitlab is supported), provide ENVs:
``` shell
export CI_API_V4_URL=ENDPOINT_HERE
export GITLAB_PRIVATE_TOKEN=TOKEN_HERE
export CI_MERGE_REQUEST_IID=MERGE_REQUEST_IID_HERE
export CI_PROJECT_ID=ID_HERE
```

## Usage

Send test results to testops
```shell
easy_allure send ./allure_reports --launch-name my_launch
```
