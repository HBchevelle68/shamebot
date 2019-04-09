import sys

# Colored printing functions for strings that use universal ANSI escape sequences.
# fail: bold red, pass: bold green, warn: bold yellow, 
# info: bold blue, bold: bold white

class ColorPrint:

    @staticmethod
    def print_fail(message, prefix="", end = '\n'):
        sys.stderr.write('\x1b[0;31m' + prefix + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, prefix="", end = '\n'):
        sys.stdout.write('\x1b[6;32m' + prefix + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, prefix="", end = '\n'):
        sys.stderr.write('\x1b[1;33m' + prefix + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, prefix="", end = '\n'):
        sys.stdout.write('\x1b[6;34m' + prefix + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, prefix="", end = '\n'):
        sys.stdout.write('\x1b[1;37m' + prefix + message.strip() + '\x1b[0m' + end)