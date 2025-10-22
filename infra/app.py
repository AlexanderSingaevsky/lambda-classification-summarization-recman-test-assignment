#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.mvp_stack import MvpStack


app = cdk.App()
env = cdk.Environment(
    account=app.node.try_get_context("account") or app.node.try_get_context("cdk_default_account"),
    region=app.node.try_get_context("region") or app.node.try_get_context("cdk_default_region"),
)

MvpStack(app, "MvpStack", env=env)

app.synth()


