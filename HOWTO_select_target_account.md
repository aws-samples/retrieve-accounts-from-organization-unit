## To select the AWS CLI and CDK target account, there is multiple possible approaches:


https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config
```
aws configure
```

or 

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
```
export AWS_ACCESS_KEY_ID=<access key, ie: AKIAIOSFODNN7EXAMPLE>
export AWS_SECRET_ACCESS_KEY=<secret, ie: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY>
export AWS_DEFAULT_REGION=<region, ie: eu-central-1>
```

or

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html#using-profiles
```
export AWS_PROFILE=<profile name>
```