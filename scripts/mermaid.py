from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        self.result.append(self.get_starttag_text())
        if tag == 'body':
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
            # Add the script tag before closing body tag
            self.result.append('''
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
for (const element of document.getElementsByClassName("language-mermaid")) {
    element.classList.add("mermaid");
}
mermaid.initialize({ startOnLoad: true });
</script>
''')
        self.result.append(f'</{tag}>')

    def handle_data(self, data):
        self.result.append(data)


# Load the HTML content
with open('./_site/index.html', 'r') as file:
    content = file.read()

# Parse the HTML content
parser = MyHTMLParser()
parser.feed(content)

# Save the modified HTML back to the file
with open('./_site/index.html', 'w') as file:
    file.write(''.join(parser.result))
