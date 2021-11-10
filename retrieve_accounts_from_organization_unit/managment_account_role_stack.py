from aws_cdk import core as cdk
from constant import Constant as c
import aws_cdk.aws_iam as iam


class ManagmentAccountRoleStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        reportingAccountIdParameter = cdk.CfnParameter(self, id="reportingAccountId"
            ,description="AWS account id of the Organization managment account, aka root account"
        )

        organizationIdParameter = cdk.CfnParameter(self, id="organizationId"
            ,description="Organization id, ie: o-abcdefg123"
        )  

        organizationUnitIdParameter = cdk.CfnParameter(self, id="organizationUnitId"
            ,description="Organization Unit id, ie: ou-abcd-abcde1234"
        )        


        trustedPrincipalARN = my_resource = cdk.Stack.of(self).format_arn(
            service="iam"
            ,region=""
            ,account=reportingAccountIdParameter.value_as_string
            ,resource="role"
            ,resource_name=c.REPORTING_ACCOUNT_ROLE_NAME
        )
        trustedPrincipal = iam.Role.from_role_arn(self, id="trustedPrincipal"
            , mutable=False
            , role_arn=trustedPrincipalARN
        )


        retrieveAccountsFromOUAdminRole = iam.Role(self, id="retrieveAccountsFromOUAdminRole"
            , role_name=c.ADMIN_ACCOUNT_ROLE_NAME
            , assumed_by=trustedPrincipal
        )


        organizationUnitARN = my_resource = cdk.Stack.of(self).format_arn(
            service="organizations"
            ,region=""
            ,account=self.account
            ,resource="ou"
            ,resource_name=organizationIdParameter.value_as_string + "/" + organizationUnitIdParameter.value_as_string
        )
        retrieveAccountsFromOUAdminRole.attach_inline_policy(
            iam.Policy(self, id="canListAccountsForParentOU"
                , policy_name="CanListAccountsForParentOU"
                , statements=[
                    iam.PolicyStatement(
                        actions=["organizations:ListAccountsForParent"]
                        , effect=iam.Effect.ALLOW
                        , resources=[organizationUnitARN]
                    )
                ]
            )
        )


        cdk.CfnOutput(self, id="outputTrustedRoleARN"
            , value=trustedPrincipalARN
        )

        cdk.CfnOutput(self, id="outputOrganizationUnitARN"
            , value=organizationUnitARN
        )

        cdk.CfnOutput(self, id="outputRetrieveAccountsFromOUAdminRoleRN"
            , value=retrieveAccountsFromOUAdminRole.role_arn
            , description="ARN of Role allowing to query Organisation"
        )
