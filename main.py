from copy import error
import sys
# DEFINE RESP (REdis Serialization Protocol) response types
ARITY = {
    "ECHO": (1,1),
    "PING": (0,1),
    "COMMAND": (0,1),
}
def check_arity(command, args):
    """Check if the number of arguments for a command is valid."""
    min_args, max_args = ARITY.get(command.upper(), (0, 0))
    if not (min_args <= len(args) <= max_args):
        return False
    return True
def bulk__string(s):
    """Return a RESP bulk string representation of the given string."""
    if s is None:
        return "$-1\r\n"
    return f"${len(s)}\r\n{s}\r\n"
def simple_string(s):
    """Return a RESP simple string representation of the given string."""
    return f"+{s}\r\n"
def error_string(msg):
    """Return a RESP error string representation of the given string."""
    return f"-{msg}\r\n"
def integer_string(i):
    """Return a RESP integer representation of the given integer."""
    return f":{i}\r\n"
def handle_command(args):
    HANDLERS = {
        "ECHO": cmd_echo,
        "PING": cmd_ping,
        "COMMAND": cmd_docs,
    }
    """Process a Redis command and return the RESP response."""
    cmd = args[0].upper()
    args = args[1:]
    handler = HANDLERS.get(cmd)
    if handler is not None and not check_arity(cmd, args):
        return error_string(f"ERR wrong number of arguments for '{cmd}' command")
    if handler is None:
        return error_string(f"ERR unknown command '{cmd}'")
    return handler(args)
def cmd_echo(args):
    """Handle the ECHO command."""
    if len(args) < 1:
        return "-ERR wrong number of arguments for 'ECHO' command\r\n"
    message = args[0]
    return bulk__string(message)

def cmd_ping(args):
    """Handle the PING command."""
    if len(args) == 0:
        return "+PONG\r\n"
    elif len(args) == 1:
        message = args[0]
        return bulk__string(message)
    else:
        return "-ERR wrong number of arguments for 'PING' command\r\n"
def cmd_docs(args):
    # """Handle the DOCS command."""
    # if len(args) != 1:
    #     return "-ERR wrong number of arguments for 'DOCS' command\r\n"
    # command = args[0].upper()
    # docs = {
    #     "ECHO": "ECHO message: Returns the message.",
    #     "PING": "PING [message]: Returns PONG or the message.",
    # }
    # if command not in docs:
    #     return error(f"-ERR unknown command '{command}'")
    return f"+OK\r\n"
    return bulk__string(docs[command])
def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        args = parse_args(line)
        response = handle_command(args)
        sys.stdout.write(response)
        sys.stdout.flush()

def parse_args(line):
    """Split a command line into arguments, handling quoted strings."""
    args = []
    current = ""
    in_quotes = False
    for ch in line:
        if ch == '"' and not in_quotes:
            in_quotes = True
        elif ch == '"' and in_quotes:
            in_quotes = False
        elif ch == ' ' and not in_quotes:
            if current:
                args.append(current)
                current = ""
        else:
            current += ch
    if current:
        args.append(current)
    return args

if __name__ == "__main__":
    main()
