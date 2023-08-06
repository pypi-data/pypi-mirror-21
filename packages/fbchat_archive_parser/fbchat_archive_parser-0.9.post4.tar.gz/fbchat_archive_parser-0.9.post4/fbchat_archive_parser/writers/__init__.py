import importlib


BUILTIN_WRITERS = ("json", "csv", "text", "yaml",)


class SerializerDoesNotExist(KeyError):
    """The requested serializer was not found."""
    pass


def write(format, data, stream):
    if format not in BUILTIN_WRITERS:
        raise SerializerDoesNotExist("No such serializer '%s'" % format)
    writer_type = importlib.import_module("fbchat_archive_parser.writers.%s"
                                          % format)
    item = getattr(writer_type, "%sWriter" % (format[0].upper() + format[1:]))
    item().write(data, stream)
