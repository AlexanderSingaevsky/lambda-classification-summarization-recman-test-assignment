from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
)
import aws_cdk as cdk
from constructs import Construct
from pathlib import Path


def _load_env_from_dotenv(dotenv_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not dotenv_path.exists():
        return env
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            env[key] = value
    return env


class MvpStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Package source + dependencies from src/requirements.txt into the Lambda artifact
        # Using bundling ensures third-party libs are installed inside the deployment package
        repo_root = Path(__file__).resolve().parents[2]
        lambda_env = _load_env_from_dotenv(repo_root / ".env")
        fn = _lambda.Function(
            self,
            "NotificationHandler",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="handler.handler",
            code=_lambda.Code.from_asset(
                "src",
                bundling=cdk.BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_13.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            environment=lambda_env,
            description="MVP placeholder Lambda for notification handling",
        )

        # Attach a public Function URL for simple invocation without API Gateway
        fn_url = fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"]
            ),
        )

        # Output the Function URL
        CfnOutput(self, "NotificationHandlerFunctionUrl", value=fn_url.url)


