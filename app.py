#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from retrieve_accounts_from_organization_unit.managment_account_role_stack import ManagmentAccountRoleStack
from retrieve_accounts_from_organization_unit.reporting_app_stack import ReportingAppStack

app = cdk.App()
ReportingAppStack(app, "ReportingAppStack",)
ManagmentAccountRoleStack(app, "ManagmentAccountRoleStack",)

app.synth()
