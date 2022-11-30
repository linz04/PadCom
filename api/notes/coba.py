import pdfkit

config = pdfkit.configuration(wkhtmltopdf = "/usr/bin/wkhtmltopdf")
pdfkit.from_url("https://google.com", "test/test.pdf", verbose=True, configuration = config)
print("="*50)