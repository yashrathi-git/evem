from premailer import transform
from mylifelogger import session_factory, BASEDIR
from mylifelogger.models import Event
from os.path import join as path_join
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from jinja2 import Template
from bs4 import BeautifulSoup


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
    short_description = content.short_description
    plugins = ['strikethrough', 'footnotes',
               'table', 'url', 'task_lists']
    markdown = mistune.create_markdown(
        renderer=HighlightRenderer(), plugins=plugins)
    html = markdown(body)

    template_file = 'email_template.html'
    # Set up jinja templates
    with open(path_join(BASEDIR, 'templates', template_file)) as file:
        template = Template(file.read())
    template_vars = {'email_content': html,
                     'title': title, 'date_created': date_created.strftime("%B %d, %Y"),
                     'short_description': short_description}
    raw_html = template.render(template_vars)

    with open(path_join(BASEDIR, 'css', 'colorful.css')) as file:
        try:
            html = str(BeautifulSoup(transform(raw_html, remove_classes=True,
                                               css_text=file.read()),
                                     'html.parser').prettify(formatter="html"))
        except Exception as e:
            print("Unable to add styles.")
            print('Exception: ' + str(e))

    with open(path_join(BASEDIR, 'markdown', 'template.html'), 'w') as file:
        file.write(html)


send_mail(7)
