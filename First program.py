import os
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

FORM_PAGE = """
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Personal Details Form</title>
	<style>
		body { font-family: Arial, sans-serif; background: #f2f4f7; margin: 0; padding: 24px; }
		main { max-width: 520px; margin: 0 auto; background: white; padding: 24px; border-radius: 12px; }
		h1 { margin-top: 0; }
		label { display: block; margin-top: 14px; font-weight: bold; }
		input { box-sizing: border-box; width: 100%; padding: 11px; margin-top: 6px; border: 1px solid #bbb; border-radius: 6px; font-size: 16px; }
		button { width: 100%; margin-top: 22px; padding: 12px; border: 0; border-radius: 6px; background: #1769aa; color: white; font-size: 16px; cursor: pointer; }
		.answers { margin-top: 24px; padding: 16px; background: #eef7ee; border-radius: 8px; }
		.answers p { margin: 8px 0; }
	</style>
</head>
<body>
<main>
	<h1>Personal Details</h1>
	<form method="post">
		<label for="name">Name</label>
		<input id="name" name="name" required>

		<label for="age">Age</label>
		<input id="age" name="age" type="number" min="1" required>

		<label for="date">Birth date</label>
		<input id="date" name="date" type="date" required>

		<label for="occupation">Occupation</label>
		<input id="occupation" name="occupation" required>

		<label for="year">Academic year</label>
		<input id="year" name="year" required>

		<label for="gender">Gender</label>
		<input id="gender" name="gender" required>

		<label for="love">Love interest</label>
		<input id="love" name="love" required>

		<button type="submit">Submit form</button>
	</form>

	<!-- ANSWERS -->
</main>
</body>
</html>
"""


class FormHandler(BaseHTTPRequestHandler):
	def send_page(self, answers=None):
		answer_section = ""
		if answers:
			answer_lines = "".join(
				f"<p><strong>{escape(label)}:</strong> {escape(value)}</p>"
				for label, value in answers.items()
			)
			answer_section = (
				'<section class="answers"><h2>Submitted answers</h2>'
				f"{answer_lines}</section>"
			)
		page = FORM_PAGE.replace("<!-- ANSWERS -->", answer_section)
		body = page.encode("utf-8")
		self.send_response(200)
		self.send_header("Content-Type", "text/html; charset=utf-8")
		self.send_header("Content-Length", str(len(body)))
		self.end_headers()
		self.wfile.write(body)

	def do_GET(self):
		self.send_page()

	def do_POST(self):
		length = int(self.headers.get("Content-Length", 0))
		values = parse_qs(self.rfile.read(length).decode("utf-8"))
		answers = {
			"Name": values.get("name", [""])[0],
			"Age": values.get("age", [""])[0],
			"Birth date": values.get("date", [""])[0],
			"Occupation": values.get("occupation", [""])[0],
			"Academic year": values.get("year", [""])[0],
			"Gender": values.get("gender", [""])[0],
			"Love interest": values.get("love", [""])[0],
		}
		self.send_page(answers)


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8000))
	print(f"Open http://127.0.0.1:{port} in your browser")
	HTTPServer(("0.0.0.0", port), FormHandler).serve_forever()    First program.py