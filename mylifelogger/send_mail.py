from premailer import transform
from mylifelogger import session_factory, BASEDIR
from mylifelogger.models import Event
from os.path import join as path_join
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'


def send_mail(id):
    session = session_factory()
    content = session.query(Event).filter_by(id=id).first()
    session.close()

    body = content.long_description
    title = content.title
    date_created = content.date_created

    plugins = ['strikethrough', 'footnotes',
               'table', 'url', 'task_lists']
    markdown = mistune.create_markdown(
        renderer=HighlightRenderer(), plugins=plugins)
    html = markdown(body)

    with open(path_join(BASEDIR, 'css', 'colorful.css')) as file:
        try:
            html = transform(html, remove_classes=True, css_text=file.read())
        except Exception as e:
            print("Unable to add styles.")
            print('Exception: ' + str(e))

    with open(path_join(BASEDIR, 'markdown', 'template.html'), 'w') as file:
        file.write(html)


send_mail(3)
