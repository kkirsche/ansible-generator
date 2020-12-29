"""The ansible_generator.cli.main module is the main entrypoint for the Ansible-Generator command-line.

The Ansible-Generator CLI's main module is used to implement a command-line builder for the
Ansible-Generator application. This attempts to implement the best practices for command-line
interfaces as outlined by https://clig.dev, https://no-color.org, and others.
"""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARNING,
    Handler,
    Logger,
    NullHandler,
    StreamHandler,
    captureWarnings,
)
from os import getenv
from sys import stdout
from typing import Dict, Optional

from pythonjsonlogger import jsonlogger
from sentry_sdk import init as sentry_sdk_init
from sentry_sdk.integrations.logging import LoggingIntegration
from structlog import configure, get_logger
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    KeyValueRenderer,
    StackInfoRenderer,
    TimeStamper,
    UnicodeDecoder,
    format_exc_info,
)
from structlog.stdlib import (
    BoundLogger,
    LoggerFactory,
    PositionalArgumentsFormatter,
    ProcessorFormatter,
    add_log_level,
    add_logger_name,
    filter_by_level,
    render_to_log_kwargs,
)

from ansible_generator.cli.builder import CommandLineBuilder
from ansible_generator.core import InfoFilter, version
from ansible_generator.error import BuildOrderError

EX_OK: int = 0  # cross-platform equivalent to os.EX_OK
EX_CONFIG: int = 78  # cross-platform equivalent to os.EX_CONFIG


class AnsibleGeneratorCLI(CommandLineBuilder):
    """AnsibleGeneratorCLI houses the Ansible-Generator command-line interface.

    The AnsibleGeneratorCLI is responsible for acting as the entry-point to the
    command-line interface for Ansible-Generator. This means that the
    AnsibleGeneratorCLI class will provide the argument parser for the CLI. It will
    then dispatch the request command.
    """

    _silence_tqdm: bool = False
    logger: Optional[BoundLogger] = None
    level_map: Dict[str, int] = {
        "debug": DEBUG,
        "info": INFO,
        "warning": WARNING,
        "error": ERROR,
        "critical": CRITICAL,
        "fatal": FATAL,
    }

    def build(self) -> None:
        """build is the public interface to build the command-line interface.

        This method is responsible for building the object's components in the
        correct order.
        """
        self._build_parser()

    def _ensure_logger(self):
        """_ensure_logger verifies the logger attribute exists.

        Raises:
            BuildOrderError: The logger was not configured.
        """
        if self.logger is None:
            raise BuildOrderError(
                "Logger is required to be built prior to other OlympusCLI attributes",
                missing_attribute="logger",
            )

    def _build_logger(
        self,
        level: str,
        json: bool,
        color: bool,
        debug: bool,
        quiet: bool,
        plain: bool,
    ) -> None:
        """_build_logger builds and configures the logging attribute.

        This function mutates the builder by adding the logger attribute.

        Parameters:
            level: The value of the --level flag;
            json: Whether the --json flag has been set;
            color: Whether the --no-color has NOT been set (inverts the no_color arg);
            debug: Whether the --debug flag has been set;
            quiet: Whether the --quiet flag has been set;
            plain: Whether the --plain flag has been set.
        """
        timestamper = TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
        shared_processors = [
            add_log_level,
            timestamper,
        ]

        if plain:
            # the user has asked us to simplify the output
            # so we remove things like timestamps, log levels, etc.
            # focusing only on the message.
            configure(
                processors=[
                    filter_by_level,
                    UnicodeDecoder(),
                    ProcessorFormatter.wrap_for_formatter,
                ],
                logger_factory=LoggerFactory(),
                wrapper_class=BoundLogger,
                cache_logger_on_first_use=True,
            )
        else:
            # normal configuration will be a bit more verbose with timestamps,
            # log levels, and other metadata. Useful though in an enterprise
            # application to have that.
            configure(
                processors=[
                    filter_by_level,
                    add_logger_name,
                    add_log_level,
                    PositionalArgumentsFormatter(),
                    format_exc_info,
                    UnicodeDecoder(),
                    ProcessorFormatter.wrap_for_formatter,
                ],
                logger_factory=LoggerFactory(),
                wrapper_class=BoundLogger,
                cache_logger_on_first_use=True,
            )

        # autodetect if we have a TTY, etc.
        crp = ConsoleRenderer()
        if not color:
            # the user has passed in --no-color, disable colors
            # commonly useful if using in a script
            crp = ConsoleRenderer(colors=False)

        console_formatter = ProcessorFormatter(
            processor=crp,
            foreign_pre_chain=shared_processors,
        )

        if plain:
            # when in plain mode, we don't want to include the timestamper
            # or the log level, so we remove the pre chain.
            console_formatter = ProcessorFormatter(
                processor=crp,
            )

        # define the types as the higher-level Handler type
        handler1: Handler
        handler2: Handler
        if not quiet or debug:
            # if we have not received -q / --quiet
            # or we have received --debug (overrides --quiet)
            # output to stdout for debug and info
            handler1 = StreamHandler(stdout)
            handler1.setLevel(DEBUG)
            handler1.addFilter(InfoFilter())
            # stderr for warnings and above
            handler2 = StreamHandler()
            handler2.setLevel(WARNING)
        else:
            # disable all logging
            handler1 = NullHandler()
            handler2 = NullHandler()

        if json:
            # structlog uses event instead of message which JsonFormatter defaults to
            handler1.setFormatter(jsonlogger.JsonFormatter("%(event)s"))
            handler2.setFormatter(jsonlogger.JsonFormatter("%(event)s"))
        else:
            handler1.setFormatter(console_formatter)
            handler2.setFormatter(console_formatter)
        self.logger: BoundLogger = get_logger(__name__)
        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)
        self.logger.setLevel(self.level_map[level])
        sentry_logging = LoggingIntegration(
            level=INFO, event_level=ERROR
        )  # hard-coded as this is remote logging
        sentry_sdk_init(
            dsn="https://036bd28e074a4a4a99712dc05c9f768e@sentry.io/202195",
            integrations=[sentry_logging],
            release=version,
        )
        captureWarnings(True)

    def _build_parser(self) -> None:
        """_build_parser is used to build the ArgumentParser.

        This function mutates the builder by creating the parser attribute.
        """
        self.parser = ArgumentParser(
            description="The Ansible-Generator command-line utility",
            epilog="Examples:\n=======",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

        application_group = self.parser.add_argument_group("Application")
        application_group.add_argument(
            "--version",
            action="store_true",
            help="Print the version number of Ansible-Generator.",
        )

        # best attempt at following CLI Guildelines
        # https://clig.dev
        logging_group = self.parser.add_argument_group("Logging")
        logging_group.add_argument(
            "-j", "--json", action="store_true", help="Output log messages using JSON."
        )
        logging_group.add_argument(
            "--debug",
            action="store_true",
            help="Output debug log messages. (same as --level debug, overrides --level, overrides --quiet)",
        )
        logging_group.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Disable all logging (overrides --level, overriden by --debug)",
        )
        logging_group.add_argument(
            "--plain", action="store_true", help="Simplify output format."
        )
        logging_group.add_argument(
            "-l", "--level", default="error", choices=list(self.level_map.keys())
        )
        # no-color.org
        # https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46
        logging_group.add_argument(
            "--no-color",
            help="Disable color in log messages.",
            action="store_true",
            dest="no_color",
            default=(getenv("NO_COLOR", False) or getenv("TERM", "") == "dumb"),
        )

        generator_group = self.parser.add_argument_group("Generator")
        generator_group.add_argument(
            "-a",
            "--alternate-layout",
            action="store_true",
            help="Create the alternate layout for Ansible.",
        )
        generator_group.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force directory and file generation.",
        )
        generator_group.add_argument(
            "--with-library",
            action="store_true",
            help="Include the custom module library folder.",
        )
        generator_group.add_argument(
            "--with-module-utils",
            action="store_true",
            help="Include the custom module_utils to support modules folder.",
        )
        generator_group.add_argument(
            "--with-filter-plugins",
            action="store_true",
            help="Include the custom filter plugins folder.",
        )
        generator_group.add_argument(
            "-i",
            "--inventories",
            nargs="+",
            default=["production", "staging"],
            type=str,
            help="The inventory locations to generate",
        )
        generator_group.add_argument(
            "-p",
            "--projects",
            nargs="+",
            default=[],
            type=str,
            help=(
                "The projects to create (must be an empty directory or a location"
                + "where this user can create folders and files)"
            ),
        )
        generator_group.add_argument(
            "-r",
            "--roles",
            nargs="+",
            default=[],
            type=str,
            help="The roles to generate (via ansible-galaxy)",
        )

    def _ensure_parser(self) -> None:
        """_ensure_parser verifies the parser attribute exists.

        Raises:
            BuildOrderError: The parser was not configured.
        """
        if self.parser is None:
            raise BuildOrderError(
                "Parser is required to be built prior to other AnsibleGeneratorCLI attributes",
                missing_attribute="parser",
            )

    def run(self) -> None:
        """run is the public interface for executing the command-line interface.

        This method will execute the command line interface. This means building the
        parser, parsing the arguments and commands, and then dispatching the action.
        """
        self._ensure_parser()
        args = self.parser.parse_args()
        if args.version:
            print(f"Version: {version}")
            raise SystemExit(EX_OK)
        if args.debug:
            args.level = "debug"
        if args.quiet or args.plain:
            self._silence_tqdm = True
        self._build_logger(
            level=args.level,
            json=args.json,
            color=(not args.no_color),
            debug=args.debug,
            quiet=args.quiet,
            plain=args.plain,
        )
        self._ensure_logger()
        self.logger.debug("Building directory generator")
        self.logger.debug("Building file/content generator")
