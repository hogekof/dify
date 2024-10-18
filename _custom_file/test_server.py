import http.server
import socketserver
import os

# ポート番号を設定
PORT = 8500

# ディレクトリを設定
web_dir = '/Users/sumou-no-oujisama/Dropbox/work/llm/dify'
os.chdir(web_dir)

# サーバーハンドラーを作成
Handler = http.server.SimpleHTTPRequestHandler

# サーバーを設定
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f'http://localhost:{PORT}')
    httpd.serve_forever()
