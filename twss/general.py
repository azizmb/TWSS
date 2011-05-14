from textwrap import TextWrapper

def pretty_print_status(status):
    status_wrapper = TextWrapper(width=60, initial_indent=' ', subsequent_indent=' ')
    print status_wrapper.fill(status.text)
    print '\n %s %s via %s\n' % (status.author.screen_name, status.created_at, status.source)
