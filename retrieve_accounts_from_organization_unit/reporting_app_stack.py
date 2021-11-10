from aws_cdk import core as cdk
from constant import Constant as c
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_logs as log

class ReportingAppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        managmentAccountIdParameter = cdk.CfnParameter(self, id="managmentAccountId"
            ,description="AWS account id of the Organization managment account, aka root account"
        )

        organisationUnitIdParameter = cdk.CfnParameter(self, id="organisationUnitId"
            ,description="Organisation Unit id, ie: ou-abcd-abcde1234"
        )    

        trustedPrincipal = iam.ServicePrincipal('lambda.amazonaws.com')
        retrieveAccountsFromOUReportingRole = iam.Role(self, id="retrieveAccountsFromOUReportingRole"
            ,role_name=c.REPORTING_ACCOUNT_ROLE_NAME
            ,assumed_by=trustedPrincipal
            ,managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
                #,iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole')
            ]
        )

        assumeableRoleARN = my_resource = cdk.Stack.of(self).format_arn(
            service="iam"
            ,region=""
            ,account=managmentAccountIdParameter.value_as_string
            ,resource="role"
            ,resource_name=c.ADMIN_ACCOUNT_ROLE_NAME
        )
        retrieveAccountsFromOUReportingRole.attach_inline_policy(
            iam.Policy(self, id="canAssumeAdminAccountRole"
                , policy_name="CanAssume"+c.ADMIN_ACCOUNT_ROLE_NAME
                , statements=[
                    iam.PolicyStatement(
                        actions=["sts:AssumeRole"]
                        , effect=iam.Effect.ALLOW
                        , resources=[assumeableRoleARN]
                    )
                ]
            )
        )

        retrieveAccountsFromOUReportingRole.attach_inline_policy(
            iam.Policy(self, id="writeLogsPolicy"
                , policy_name="CanWriteLogsPolicy"
                , statements=[
                    iam.PolicyStatement(
                        actions=[
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"                
                        ]
                        , effect=iam.Effect.ALLOW
                        , resources=["*"]
                    )                    
                ]
            )
        )


         


        cdk.CfnOutput(self, id="outputAssumeableRoleARN"
            , value=assumeableRoleARN
        )


        cdk.CfnOutput(self, id="outputRetrieveAccountsFromOUReportingRoleARN"
            , value=retrieveAccountsFromOUReportingRole.role_arn
        )


        # Defines the AWS Lambda reporting app
        reportingLambdaFunction = _lambda.Function(self, "reportingLambdaFunction"
            ,runtime=_lambda.Runtime.PYTHON_3_7
            ,function_name='log-organization-unit-accounts-id'
            ,description='Lambda function that retrieve and log all account-id in an Organization Unit'
            ,code=_lambda.Code.asset('src/functions')
            ,handler='logOUAccountsId.lambda_handler'
            ,role=retrieveAccountsFromOUReportingRole
            ,log_retention=log.RetentionDays.ONE_DAY
        )
        reportingLambdaFunction.add_environment(
            key="ASSUME_ROLE_ARN"
            ,value=assumeableRoleARN
        )
        reportingLambdaFunction.add_environment(
            key="ORGANISATION_UNIT_ID"
            ,value=organisationUnitIdParameter.value_as_string
        )

