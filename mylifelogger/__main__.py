import click
from colorama import init, Fore, Style
import re
from mylifelogger.models import parse_date, ReminderDates, Event
import datetime
from mylifelogger import BASEDIR
from os.path import join as path_join
from dateutil.relativedelta import relativedelta


def parse_remind_syntax(code):
    pattern = r'period[ ]*=[ ]*([0-9]+)-(day|year|month|days|months|years)[ ]*,[ ]*repeat[ ]*=[ ]*([0-9*]+)'
    tree = re.findall(pattern, code)

    try:
        assert len(tree[0]) == 3
        tree[0] = list(tree[0])
        tree[0][0] = int(tree[0][0])
    except:
        print(tree)
        raise click.UsageError(f'"{code}" is not a valid command')
    if tree[0][1] == 'year' or tree[0][1] == 'years':
        tdelta = relativedelta(years=tree[0][0])
    elif tree[0][1] == 'month' or tree[0][1] == 'months':
        tdelta = relativedelta(months=tree[0][0])
    elif tree[0][1] == 'days' or tree[0][1] == 'day':
        tdelta = relativedelta(days=tree[0][0])

    repeat = tree[0][2]
    repeat = True if repeat == '*' else int(repeat)
    return tdelta, repeat


def prompt(text):
    user_input = input(
        f'{Fore.RED}{Style.BRIGHT}?{Style.RESET_ALL} {text}: {Fore.CYAN}')
    print(Style.RESET_ALL, end='')
    return user_input


@click.group()
@click.version_option()
def cli():
    """
        Creates events that are reminded to user periodically on configured email address.
    """
    pass


@cli.group()
def event():
    """
        Add, list, delete and edit events
    """
    pass


@event.command("new")
@click.option("-m", "--markdown", is_flag=True,
              help="Generate new event from markdown.")
def new(markdown):
    """
        Create new event
    """
    if not markdown:
        print(f'{Fore.MAGENTA}Date Format: dd-mm-yyyy')
        print(
            f'Leave any date field empty for today\'s date{Style.RESET_ALL}\n')
        title = prompt('title')
        short_description = prompt('short-description')
        date_created = prompt('date-of-event')
        base_date = prompt('base-date')

        if not short_description:
            short_description = title
        if not date_created:
            date_created = None
        if not base_date:
            base_date = datetime.date.today()
        else:
            base_date = parse_date(base_date)

        examples = [(f"period = 10-day, repeat = 11 "
                     f"{Fore.WHITE}# Repeat every 10 days for 11 times.{Style.RESET_ALL}"),
                    (f"period = 1-year, repeat = * "
                     f"{Fore.WHITE}# Repeat every year.{Style.RESET_ALL}")]
        print(
            f'\n{Fore.MAGENTA}Date are calculated for time after `base-date`{Style.RESET_ALL}')
        print()
        print('Examples: ')
        print(*examples, sep='\n')
        print()
        print(f'{Fore.MAGENTA}Enter q to exit{Style.RESET_ALL}\n')

        event = Event(title, short_description,
                      long_description='', date_created=date_created)
        model_objects = [event]
        while True:
            date = prompt('remind-on')
            if len(model_objects) >= 2 and date.lower() == 'q':
                break
            tdelta, repeat = parse_remind_syntax(date)
            reminder_date = tdelta + base_date
            print((f'{Fore.RED}next reminder on => {reminder_date.strftime("%d-%m-%Y")}'
                   f'{Style.RESET_ALL}'))
            if repeat == True:
                reminder = ReminderDates(event=event, time_delta=tdelta, repeat_forever=repeat,
                                         date=reminder_date)
            else:
                reminder = ReminderDates(event=event, time_delta=tdelta, repeat=repeat,
                                         date=reminder_date)
            model_objects.append(reminder)

        markdown_file = path_join(BASEDIR, 'markdown/description.md')
        with open(markdown_file) as file:
            file.write('')
        print(f'{Style.DIM}Created `description.md` file')
        print('Run following commands to complete event creation:')
        print(f'Edit the file with suitable description{Style.RESET_ALL}')
        print(f'\t{Style.DIM}nano {markdown_file}{Style.RESET_ALL}')
        print(f'\t{Style.DIM}mll event new --markdown{Style.RESET_ALL}')


if __name__ == '__main__':
    init()
