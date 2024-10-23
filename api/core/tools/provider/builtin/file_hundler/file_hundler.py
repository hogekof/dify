from typing import Any

# from core.tools.errors import ToolProviderCredentialValidationError
# from core.tools.provider.builtin.buil.tools.file_output import FileOutputTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class FileOutputProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        pass
        # try:
        #     FileOutputTool().invoke(
        #         user_id="",
        #         tool_parameters={
        #             "binary_file": b"test",
        #             "mime_type": "text/plain",
        #         },
        #     )
        # except Exception as e:
        #     raise ToolProviderCredentialValidationError(str(e))
