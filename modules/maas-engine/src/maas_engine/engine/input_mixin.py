import maas_model


class InputMixinEngine:
    """Mixin for data loading from payload"""

    def get_input_model(self, message: maas_model.MAASMessage):
        """Get the model class from the message. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            class: Model DAO class
        """
        return self.get_model(message.document_class)

    def _load_input_documents(self, payload: maas_model.MAASMessage):
        """Populate input_model and input_documents attributes

        Args:
            payload (maas_model.MAASMessage): message payload
        """
        self.logger.debug("Loading input documents")
        # get source model from payload
        self.input_model = self.get_input_model(payload)

        # load all documents, as a list to check all are present and log a meaningful
        # message if some are missing.
        # as all documents are already retrieved by the underlying execute() and not
        # scan(), there is no real memory impact.
        #
        # put the list in a class cache so a sequence of engine won't reload
        # at each run() call. Note that this cache shall be cleared at the end of the
        # execution sequence
        # child classes will have to use report() method to explicitly tell a document
        # modification is notified on the amqp bus
        self.input_documents = self.get_input_documents(payload)

        if not all(self.input_documents):
            # this is really bad: raw documents have been deleted since the payload
            # have been sent, or the document class or identifiers are wrong !
            missing = set(payload.document_ids) - {
                document.meta.id for document in self.input_documents if document
            }

            self.logger.critical(
                "Some input documents %s are missing: %s", self.input_model, missing
            )

            # purify the input
            self.input_documents = [
                document for document in self.input_documents if document
            ]
