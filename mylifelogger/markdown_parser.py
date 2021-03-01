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
import smtplib
from email.message import EmailMessage
import datetime
from humanize import naturaldelta
from colorama import Fore, Style
from click import UsageError
import os

EMAIL_ADDRESS = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('PASSWORD')


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

    if content is None:
        raise UsageError(f'No event with ID : {id}')

    _send_mail(content.title, content.html,
               send_to='yashrathicricket@gmail.com')


def _send_mail(title, html, send_to):
    msg = EmailMessage()
    msg['Subject'] = title
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = send_to
    msg.add_header('Content-Type', 'text/html')

    msg.set_content(html, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def parse_markdown(content):
    body = content.long_description
    title = content.title
    date_created = content.date_created
    short_description = content.short_description
    # Calculate time since event in human readable format
    time_since = datetime.date.today() - date_created
    time_since = naturaldelta(time_since)

    plugins = ['strikethrough', 'footnotes',
               'table', 'url', 'task_lists']

    print('Parsing Markdown...')
    markdown = mistune.create_markdown(
        renderer=HighlightRenderer(escape=False), plugins=plugins)
    html = markdown(body)
    print(f'{Style.BRIGHT}{Fore.GREEN}(\u2713){Style.RESET_ALL} Markdown converted to html.')

    # Template variables
    template_vars = {'title': title,
                     'date_created': date_created.strftime("%B %d, %Y"),
                     'short_description': short_description,
                     'time_since': time_since}
    # Setup jinja template for markdown
    print('Rendering event description...')
    html = Template(html).render(template_vars)
    print(f'{Style.BRIGHT}{Fore.GREEN}(\u2713){Style.RESET_ALL} Rendered event description.')
    # Set up jinja template for main content
    template_vars['email_content'] = html
    template_file = 'email_template.html'
    with open(path_join(BASEDIR, 'templates', template_file)) as file:
        template = Template(file.read())

    print('Enhancing html for better email content.')
    raw_html = template.render(template_vars)

    with open(path_join(BASEDIR, 'css', 'colorful.css')) as file:
        try:
            html = str(BeautifulSoup(transform(raw_html, remove_classes=True,
                                               css_text=file.read(),
                                               disable_validation=True),
                                     'html.parser').prettify(formatter="html"))
        except Exception as e:
            print("Unable to add styles.")
            print('Exception: ' + str(e))

    html_preview = path_join(BASEDIR, 'markdown', 'preview.html')
    with open(html_preview, 'w') as file:
        file.write(html)
    print(f'{Style.BRIGHT}{Fore.GREEN}(\u2713){Style.RESET_ALL} Uses inline'
          ' styling and syntax highlighting')
    print('HTML preview is available at: ')
    print(html_preview)
    return html
