from http.server import BaseHTTPRequestHandler, HTTPServer
from html import escape
from urllib.parse import parse_qs

from needleman_wunsch import chiso_needleman_wunsch


CHISO_HOST = "127.0.0.1"
CHISO_PORT = 8765


def chiso_build_match_line(chiso_aligned_one, chiso_aligned_two):
    chiso_symbols = []

    for chiso_left, chiso_right in zip(chiso_aligned_one, chiso_aligned_two):
        if chiso_left == chiso_right:
            chiso_symbols.append("|")
        elif chiso_left == "-" or chiso_right == "-":
            chiso_symbols.append(" ")
        else:
            chiso_symbols.append(".")

    return "".join(chiso_symbols)


def chiso_render_matrix(chiso_matrix, chiso_first_sequence, chiso_second_sequence):
    chiso_header_cells = ["<th></th>", "<th>-</th>"]
    for chiso_base in chiso_second_sequence:
        chiso_header_cells.append(f"<th>{escape(chiso_base)}</th>")

    chiso_rows = [f"<tr>{''.join(chiso_header_cells)}</tr>"]

    for chiso_index, chiso_score_row in enumerate(chiso_matrix):
        if chiso_index == 0:
            chiso_label = "-"
        else:
            chiso_label = chiso_first_sequence[chiso_index - 1]

        chiso_cells = [f"<th>{escape(chiso_label)}</th>"]
        for chiso_cell in chiso_score_row:
            chiso_cells.append(f"<td>{chiso_cell}</td>")

        chiso_rows.append(f"<tr>{''.join(chiso_cells)}</tr>")

    return f"<table>{''.join(chiso_rows)}</table>"


def chiso_render_page(chiso_first_sequence="", chiso_second_sequence="", chiso_result=None, chiso_error=""):
    chiso_result_html = ""

    if chiso_error:
        chiso_result_html = f"""
        <section class="notice">
            <strong>Check your input</strong>
            <p>{escape(chiso_error)}</p>
        </section>
        """

    if chiso_result:
        chiso_aligned_one, chiso_aligned_two, chiso_score, chiso_matrix = chiso_result
        chiso_match_line = chiso_build_match_line(chiso_aligned_one, chiso_aligned_two)
        chiso_matrix_html = chiso_render_matrix(chiso_matrix, chiso_first_sequence, chiso_second_sequence)

        chiso_result_html = f"""
        <section class="result-panel">
            <div class="score-block">
                <span>Alignment Score</span>
                <strong>{chiso_score}</strong>
            </div>

            <div class="alignment-box" aria-label="Best global alignment">
                <pre>{escape(chiso_aligned_one)}
{escape(chiso_match_line)}
{escape(chiso_aligned_two)}</pre>
            </div>

            <div class="matrix-wrap">
                {chiso_matrix_html}
            </div>
        </section>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Needleman-Wunsch Alignment</title>
    <style>
        :root {{
            color-scheme: light;
            --ink: #16201d;
            --muted: #5f6b66;
            --line: #d5ddd9;
            --panel: #ffffff;
            --field: #f7faf8;
            --accent: #0f766e;
            --accent-dark: #115e59;
            --warn: #fff2d6;
            --warn-line: #f1c86d;
            --page: #eef5f2;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            color: var(--ink);
            background:
                linear-gradient(135deg, rgba(15, 118, 110, 0.14), transparent 34%),
                linear-gradient(315deg, rgba(188, 108, 37, 0.13), transparent 36%),
                var(--page);
        }}

        main {{
            width: min(1120px, calc(100% - 32px));
            margin: 0 auto;
            padding: 32px 0;
        }}

        .app-shell {{
            display: grid;
            grid-template-columns: minmax(280px, 380px) minmax(0, 1fr);
            gap: 20px;
            align-items: start;
        }}

        .input-panel,
        .result-panel,
        .notice {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 18px 45px rgba(31, 49, 43, 0.08);
        }}

        .input-panel {{
            padding: 22px;
        }}

        h1 {{
            margin: 0 0 8px;
            font-size: 30px;
            line-height: 1.1;
            letter-spacing: 0;
        }}

        .lede {{
            margin: 0 0 22px;
            color: var(--muted);
            line-height: 1.5;
        }}

        label {{
            display: block;
            margin: 16px 0 8px;
            font-weight: 700;
        }}

        textarea {{
            width: 100%;
            min-height: 92px;
            resize: vertical;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 12px;
            background: var(--field);
            color: var(--ink);
            font: 16px Consolas, "Courier New", monospace;
            letter-spacing: 0;
        }}

        textarea:focus {{
            outline: 3px solid rgba(15, 118, 110, 0.22);
            border-color: var(--accent);
        }}

        .settings {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 16px;
        }}

        .settings input {{
            width: 100%;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 10px;
            background: var(--field);
            font-size: 15px;
        }}

        button {{
            width: 100%;
            min-height: 46px;
            margin-top: 18px;
            border: 0;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
        }}

        button:hover {{
            background: var(--accent-dark);
        }}

        .notice {{
            padding: 18px;
            background: var(--warn);
            border-color: var(--warn-line);
        }}

        .notice p {{
            margin: 8px 0 0;
        }}

        .result-panel {{
            padding: 20px;
            overflow: hidden;
        }}

        .score-block {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--line);
        }}

        .score-block span {{
            color: var(--muted);
            font-weight: 700;
        }}

        .score-block strong {{
            font-size: 38px;
            line-height: 1;
            color: var(--accent-dark);
        }}

        .alignment-box {{
            margin-top: 16px;
            padding: 16px;
            border-radius: 8px;
            background: #101817;
            color: #eaf7f3;
            overflow-x: auto;
        }}

        pre {{
            margin: 0;
            font: 18px Consolas, "Courier New", monospace;
            line-height: 1.55;
            letter-spacing: 0;
        }}

        .matrix-wrap {{
            margin-top: 16px;
            overflow: auto;
            border: 1px solid var(--line);
            border-radius: 8px;
            max-height: 430px;
        }}

        table {{
            width: 100%;
            min-width: 520px;
            border-collapse: collapse;
            background: white;
        }}

        th,
        td {{
            border: 1px solid var(--line);
            padding: 9px 10px;
            text-align: center;
            font: 15px Consolas, "Courier New", monospace;
        }}

        th {{
            position: sticky;
            top: 0;
            background: #e9f2ef;
            color: #163a35;
            z-index: 1;
        }}

        td {{
            background: #fff;
        }}

        .empty-state {{
            min-height: 360px;
            display: grid;
            place-items: center;
            color: var(--muted);
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.7);
            border: 1px dashed var(--line);
            border-radius: 8px;
        }}

        @media (max-width: 820px) {{
            main {{
                width: min(100% - 22px, 680px);
                padding: 18px 0;
            }}

            .app-shell {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 25px;
            }}

            .settings {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <main>
        <div class="app-shell">
            <section class="input-panel">
                <h1>Needleman-Wunsch Alignment</h1>
                <p class="lede">Enter two DNA, RNA, or protein sequences to calculate their best global alignment.</p>

                <form method="post">
                    <label for="first_sequence">First sequence</label>
                    <textarea id="first_sequence" name="first_sequence" required>{escape(chiso_first_sequence)}</textarea>

                    <label for="second_sequence">Second sequence</label>
                    <textarea id="second_sequence" name="second_sequence" required>{escape(chiso_second_sequence)}</textarea>

                    <div class="settings">
                        <label>
                            Match
                            <input type="number" name="match_score" value="1">
                        </label>
                        <label>
                            Mismatch
                            <input type="number" name="mismatch_score" value="-1">
                        </label>
                        <label>
                            Gap
                            <input type="number" name="gap_penalty" value="-2">
                        </label>
                    </div>

                    <button type="submit">Align sequences</button>
                </form>
            </section>

            <div>
                {chiso_result_html if chiso_result_html else '<div class="empty-state">Your alignment result will appear here after you submit two sequences.</div>'}
            </div>
        </div>
    </main>
</body>
</html>"""


class ChisoNeedlemanHandler(BaseHTTPRequestHandler):
    def chiso_send_html(self, chiso_html, chiso_status=200):
        chiso_payload = chiso_html.encode("utf-8")
        self.send_response(chiso_status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(chiso_payload)))
        self.end_headers()
        self.wfile.write(chiso_payload)

    def do_GET(self):
        self.chiso_send_html(chiso_render_page())

    def do_POST(self):
        chiso_length = int(self.headers.get("Content-Length", 0))
        chiso_body = self.rfile.read(chiso_length).decode("utf-8")
        chiso_form = parse_qs(chiso_body)

        chiso_first_sequence = chiso_form.get("first_sequence", [""])[0].upper().replace(" ", "").replace("\r", "").replace("\n", "")
        chiso_second_sequence = chiso_form.get("second_sequence", [""])[0].upper().replace(" ", "").replace("\r", "").replace("\n", "")

        try:
            chiso_match_score = int(chiso_form.get("match_score", ["1"])[0])
            chiso_mismatch_score = int(chiso_form.get("mismatch_score", ["-1"])[0])
            chiso_gap_penalty = int(chiso_form.get("gap_penalty", ["-2"])[0])
        except ValueError:
            chiso_html = chiso_render_page(
                chiso_first_sequence,
                chiso_second_sequence,
                chiso_error="Scores must be whole numbers.",
            )
            self.chiso_send_html(chiso_html, 400)
            return

        if not chiso_first_sequence or not chiso_second_sequence:
            chiso_html = chiso_render_page(
                chiso_first_sequence,
                chiso_second_sequence,
                chiso_error="Both sequence fields are required.",
            )
            self.chiso_send_html(chiso_html, 400)
            return

        chiso_result = chiso_needleman_wunsch(
            chiso_first_sequence,
            chiso_second_sequence,
            chiso_match_score,
            chiso_mismatch_score,
            chiso_gap_penalty,
        )
        chiso_html = chiso_render_page(chiso_first_sequence, chiso_second_sequence, chiso_result)
        self.chiso_send_html(chiso_html)

    def log_message(self, chiso_format, *chiso_args):
        return


if __name__ == "__main__":
    chiso_server = HTTPServer((CHISO_HOST, CHISO_PORT), ChisoNeedlemanHandler)
    print(f"Open http://{CHISO_HOST}:{CHISO_PORT} in your browser")
    chiso_server.serve_forever()
