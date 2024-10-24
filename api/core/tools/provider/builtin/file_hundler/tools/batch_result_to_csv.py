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
        meta = {'mime_type': 'text/csv'}
        try:
            # データをDataFrameに変換
            df = pd.DataFrame([json.loads(x[:x.find('}') + 1]) for x in content.split('\t') if x.find('{') >= 0])

            # StringIOオブジェクトを作成
            csv_buffer = io.BytesIO()

            # DataFrameをCSV形式で書き込み（ファイルに書き込まずにメモリ上に）
            df.to_csv(csv_buffer, index=False)

            blob = csv_buffer.getvalue()  # バイナリデータを取得

            import csv
            from io import StringIO

            # Create CSV data in memory
            csv_output = StringIO()
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(["Name", "Age", "City"])
            csv_writer.writerow(["Alice", "30", "New York"])
            csv_writer.writerow(["Bob", "25", "Los Angeles"])
            csv_writer.writerow(["Charlie", "35", "Chicago"])

            csv_content = csv_output.getvalue()
            csv_output.close()

            responses = [
                self.create_blob_message(blob=blob, meta=meta, save_as="result.csv"),
                self.create_blob_message(blob=csv_content.encode('utf-8'), meta=meta, save_as="result2.csv"),
                self.create_blob_message(blob='a,b,c', meta=meta, save_as="result3.csv"),
            ]
            return responses
        except Exception as e:
            return self.create_text_message(f"Failed to file output, error: {str(e)}")
