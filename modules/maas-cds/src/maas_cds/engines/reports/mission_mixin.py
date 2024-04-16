"""Mission dedicated tools"""

import maas_model

from maas_cds import model


class MissionMixinEngine:
    """
    A mixin class for RawDataEngine to send report message to mission-dedicated queues
    with mission dedicated class.

    Document classes shall have a 'mission' attribute !
    """

    def get_report_action(
        self, es_result: str, document: maas_model.MAASDocument
    ) -> str:
        """Override.

        The action for product is suffixed by the mission to separate calculation.

        Args:
            es_result (str): opensearchpy search action result
            document (maas_model.MAASDocument): mission-enabled document

        Returns:
            str: action (routing key)
        """
        if not document.mission:
            self.logger.info(
                "No mission found for document %s - %s", document, document.name
            )
            # no report will be generated
            return None

        action = super().get_report_action(es_result, document)

        return f"{action}-{document.mission.lower()}"

    def get_report_document_classname(self, document: maas_model.MAASDocument) -> str:
        """Override to precise product subclass in message payload:
            CdsProductS1 for S1 product, etc ...

        Args:
            document (maas_model.MAASDocument): document

        Returns:
            str: mission-based document class name
        """
        classname = super().get_report_document_classname(document)

        if document.mission:
            childname = f"{classname}{document.mission.upper()}"

            if hasattr(model, childname):
                classname = childname
            else:
                self.logger.warning("Dedicated class %s not found in model", childname)
        else:
            self.logger.info(
                "No mission found for document  %s - %s", document, document.name
            )

        return classname
