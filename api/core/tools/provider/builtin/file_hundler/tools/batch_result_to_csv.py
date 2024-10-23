import io
import json
from typing import Any

import pandas as pd

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class BatchResultToCsvTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:

        content = tool_parameters['batch_result_string']
        if 'mime_type' in tool_parameters:
            meta = {'mime_type': tool_parameters['mime_type']}
        else:
            meta = None
        try:
            # データをDataFrameに変換
            df = pd.DataFrame([json.loads(x[:x.find('}') + 1]) for x in content.split('\t') if x.find('{') >= 0])

            # StringIOオブジェクトを作成
            csv_buffer = io.BytesIO()

            # DataFrameをCSV形式で書き込み（ファイルに書き込まずにメモリ上に）
            df.to_csv(csv_buffer, index=False)

            blob = csv_buffer.getvalue()  # バイナリデータを取得
            return self.create_blob_message(blob=blob, meta=meta)
        except Exception as e:
            return self.create_text_message(f"Failed to file output, error: {str(e)}")
