import time
from abc import ABCMeta, abstractmethod
from random import random

__all__ = ['HealthCheckMixin']


class HealthCheckMixin(metaclass=ABCMeta):
    """
    Adds health checking behavior to Main classes. To do that is necessary to define a health_check method responsible
    of return the current status of the application.

    This mixin also adds a new parameter ``-r``, ``--retry`` that defines the number of retries done after a failure.
    These retries uses an exponential backoff to calculate timing.
    """

    def add_arguments(self, parser: 'argparse.ArgumentParser'):
        parser.add_argument('-r', '--retry', help='Health check retries before run command. Disabled with 0, max 5.',
                            type=int, default=5, choices=range(6))

    @abstractmethod
    def health_check(self):
        """
        Does a health check.

        :return: True if health check was successful. False otherwise.
        """
        pass

    def _health_check(self):
        """
        Does a health check and retry using exponential backoff if it fails.

        :return: True if health check was successful. False otherwise.
        """
        if self.args.retry:
            health = False
            self.cli.logger.info('Performing healthcheck...')
            timeout = random()

            for i in (i for i in range(self.args.retry) if not health):
                if not self.health_check():
                    self.cli.logger.warning('Health check failed, retrying ({}/{})'.format(i + 1, self.args.retry))
                    time.sleep(timeout)
                    timeout *= 2.
                else:
                    # Healthcheck successful
                    health = True

            if not health:
                self.cli.logger.error('Retry attempts exceeded, health check failed')
        else:
            health = True

        return health

    def run(self, *args, **kwargs):
        """
        Run specified command through system arguments.

        Before running the command, a health check function will be called and if result is not successful, the command
        will be aborted.

        Arguments that have been parsed properly will be passed through \**kwargs. Unknown arguments will be passed as a
        list of strings through \*args.

        This method will print a header and the return code.
        """
        self.cli.print_header(command=self.args.command, settings=self.settings)

        if not args and not kwargs:
            args = self.unknown_args
            kwargs = vars(self.args)

        if self._health_check():
            return_code = self.run_command(self.args.command, *args, **kwargs)
        else:
            return_code = 1

        self.cli.print_return(return_code)
        return return_code
