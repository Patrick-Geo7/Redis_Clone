import sys

def bulk__string(s):
    """Return a RESP bulk string representation of the given string."""
    return f"${len(s)}\r\n{s}\r\n"

def handle_command(args):
    HANDLERS = {
        "ECHO": cmd_echo,
        "PING": cmd_ping,
    }
    """Process a Redis command and return the RESP response."""
    cmd = args[0].upper()
    args = args[1:]

    if cmd in HANDLERS:
        return HANDLERS[cmd](args)
    return "-ERR unknown command\r\n"
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
