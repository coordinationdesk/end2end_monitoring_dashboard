"""Collector Journal related stuff"""

import datetime
import logging

import opensearchpy.exceptions
import opensearchpy

from maas_model import ZuluDate

from maas_collector.rawdata.exceptions import CollectorException


class CollectingInProgressError(CollectorException):
    """
    Raised when attempting to collect an interface that is already
    beeing collected by another process or pod
    """


class NoRefreshException(CollectorException):
    """
    Raised when attempting to collect an interface that has already been collected
    """


class JournalDocument(opensearchpy.Document):
    """
    A database document to store informations about a collector's life:

     - the last time it ran: last_collect_date

     - the date of the last ingestion in a business view, like production or
       publication date


    """

    class Index:
        "opensearch meta"
        name = "maas-collector-journal"

    tick_collect_date = ZuluDate(default_timezone="UTC")

    last_collect_date = ZuluDate(default_timezone="UTC")

    last_date = ZuluDate()

    key = opensearchpy.Keyword()


class CollectorJournal:
    """CollectorJournal is a context manager that uses database document to
    store activities and to provide mutual exclusion.

    Provide ActionIterator callback to store the max value of a date field, provideded
    as constructor parameter
    """

    DOCUMENT_CLASS = JournalDocument

    def __init__(self, config, timeout: int = 10):
        self.config = config

        self.timeout = timeout

        self.document = None

        self.__max_date = None

        self.__start_date = None

        self.is_a_replay_journal = False

        self.refresh_delta = datetime.timedelta(minutes=config.refresh_interval)

        self.logger = logging.getLogger(
            self.config.interface_name + self.__class__.__name__
        )

    @property
    def journal(self):
        """lazy create / get Journal document instance"""
        if self.document is None:
            self.load()
        return self.document

    @property
    def last_date(self):
        """last meaningful date (like production / publication)"""
        return self.journal.last_date

    @property
    def id(self):
        return self.config.interface_name

    @last_date.setter
    def last_date(self, last_date):
        """set last meaningful date (like production / publication)"""
        if not self.journal.last_date or last_date > self.journal.last_date:
            self.journal.last_date = last_date

    def __enter__(self):
        # store first loop start date before i/o to not add later delay
        self.__start_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.logger.debug("set start date to %s", self.__start_date)

        self.load()

        if not self.needs_refresh():
            # nb: quite a defensive programming style
            raise NoRefreshException()

        if self.document.tick_collect_date is not None:
            now = datetime.datetime.now(tz=datetime.timezone.utc)

            if now - self.document.tick_collect_date < datetime.timedelta(
                minutes=self.timeout
            ):
                raise CollectingInProgressError(
                    f"{self.config.interface_name} is already being collected "
                    f"since {self.document.tick_collect_date}"
                )

            self.logger.info(
                "Restoring collect on interface %s", self.config.interface_name
            )
            self.logger.info("Another collector instance may have crashed or timed out")

        self.tick()

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """writes to database"""
        if exc_type and not self.is_a_replay_journal:
            # if some errors happen, do no store DOI so no gap happens in data
            # period will be completly reprocessed
            self.__max_date = None

        self.write()

    def iter_callback(self, document):
        """callback for action iterator to store the most recent production date"""
        try:
            # allow use of deep attribute
            # value = document
            # for attrname in self.config.date_attr.split("."):
            #     value = getattr(value, attrname)
            value = getattr(document, self.config.date_attr)
        except AttributeError:
            self.logger.error(
                "Document %s has no attribute %s", document, self.config.date_attr
            )
        else:
            if self.__max_date:
                self.__max_date = max(self.__max_date, value)
            else:
                self.__max_date = value

    def load(self):
        """create or read JournalDocument"""
        try:
            self.logger.debug(
                "Try accessing collector journal entry for %s",
                self.id,
            )
            self.document = self.DOCUMENT_CLASS.get(self.id)

        except opensearchpy.exceptions.NotFoundError:
            self.logger.info(
                "Creating collector journal entry for %s",
                self.id,
            )
            self._create_document_instance()

            self.document.save(refresh=True)

    def _create_document_instance(self):
        # create journal entry on demand
        self.document = self.DOCUMENT_CLASS()
        self.document.key = self.id
        self.document.meta.id = self.id

    def tick(self):
        """
        tick opensearch by setting the update_date to not be considered as timeout
        """
        self.document.tick_collect_date = datetime.datetime.now(
            tz=datetime.timezone.utc
        )

        self.logger.debug(
            "Setting tick_collect_date to %s", self.document.tick_collect_date
        )

        try:
            if self.__max_date:
                # save max date of interest
                self.document.last_date = self.__max_date

            self.document.save(refresh=True)

        except opensearchpy.exceptions.ConflictError as error:
            # dismiss document
            self.document = None
            raise CollectingInProgressError(
                f"{self.config.interface_name} is already being collected."
            ) from error

    def _fill_journal(self):
        if not self.document:
            self.logger.debug(
                "No journal to save: dismissed by conflict or other internal error"
            )
            self.__start_date = None
            return

        if self.__max_date:
            # save max date of interest
            self.document.last_date = self.__max_date
        else:
            self.logger.debug("No most recent date of interest found: no new data")

        # set the last date collect started
        self.document.last_collect_date = (
            self.__start_date
            if self.__start_date
            else datetime.datetime.now(tz=datetime.timezone.utc)
        )

        # drop tick attribute
        self.document.tick_collect_date = None

        # clear internal attribute
        self.__start_date = None

    def write(self):
        """store to opensearch"""
        self._fill_journal()

        self.document.save(refresh=True)

    def needs_refresh(self) -> bool:
        """Tell if the interface needs to be updated"""
        if self.document.last_collect_date:
            collect_delta_seconds = round(
                (
                    datetime.datetime.now(tz=datetime.timezone.utc)
                    - self.document.last_collect_date
                ).total_seconds()
            )
            self.logger.debug(
                "collect_delta_seconds: %ss refresh_delta: %s",
                collect_delta_seconds,
                self.refresh_delta,
            )
            return collect_delta_seconds >= self.refresh_delta.total_seconds()

        # first run
        self.logger.debug("needs_refresh: first run for this interface")
        return True


class ReplayJournalDocument(JournalDocument):
    """
    A document to store informations about a collector's replay run that extends
    JournalDocument with replay parameters
    """

    class Index:
        "database meta"
        name = "maas-collector-replay-journal"

    start_date = ZuluDate(default_timezone="UTC")

    end_date = ZuluDate(default_timezone="UTC")

    completed = opensearchpy.Boolean()

    nb_of_retry = opensearchpy.Integer()


class CollectorReplayJournal(CollectorJournal):
    """

    A journal for replay
    """

    DOCUMENT_CLASS = ReplayJournalDocument

    def __init__(
        self,
        config,
        start_date,
        end_date,
        suffix=None,
        timeout: int = 10,
        nb_of_retry: int = 0,
    ):
        super().__init__(config)
        self.start_date = start_date
        self.end_date = end_date
        self.is_a_replay_journal = True
        self.suffix = suffix
        self.nb_of_retry = nb_of_retry

    @property
    def id(self):
        if self.suffix:
            return f"{self.config.interface_name}_{self.suffix}"
        return super().id

    def _create_document_instance(self):
        super()._create_document_instance()
        self.document.start_date = self.start_date
        self.document.end_date = self.end_date
        self.document.completed = False
        self.document.nb_of_retry = 0

    def complete(self):
        """

        Set the completed attribute of the document to True and save
        """
        self.document.completed = True
        self.document.save(refresh=True)

    def needs_refresh(self) -> bool:
        return True

    def write(self):
        """store to opensearch"""
        self.document.nb_of_retry = self.nb_of_retry
        super().write()
