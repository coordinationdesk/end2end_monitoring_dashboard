import functools


import maas_cds.lib.parsing_name.utils as utils


class ProductDatatakeMixin:
    """

    Mixin for entities that receive attributes from datatake
    """

    @functools.cached_property
    def name_without_extension(self) -> str:
        """
        To reuse datatakes at consolidation time, as product have no extension and
        publication have one, the only way to reuse datatake cache is by using the name
        without extension.

        As it is a stable data for a run, this property is cached.

        For DD production consolidation, as name is not consolidated, DD name will be
        used for links

        Returns:
            str: name without extension if any
        """
        try:
            return utils.remove_extension_from_product_name(self.name)
        except TypeError:
            # DD consolidation does not fill product name, so name is None, try another
            # attribute as fallback strategy
            for name in ("ddip_name", "dddas_name"):
                if hasattr(self, name):
                    value = getattr(self, name)
                    if value:
                        return utils.remove_extension_from_product_name(value)

    def fill_from_datatake(self, datatake):
        """Fill document attributes with datatake info"""
        if datatake is not None and datatake != utils.DATATAKE_ID_MISSING_VALUE:
            self.datatake_id = datatake.datatake_id
            self.timeliness = datatake.timeliness
            self.absolute_orbit = datatake.absolute_orbit
            self.instrument_mode = datatake.instrument_mode

    def find_nearest_datatake(self, datatakes, tolerance=0):
        """Find the nearest datatake of the product

        Note:
            Usefull for S2

        Args:
            datatakes (CdsDatatake): A list of datatake

        Returns:
            CdsDatatake: The neareset datatake
        """
        if len(datatakes) == 0:
            return None

        product_start_date = self.sensing_start_date.timestamp()
        product_end_date = self.sensing_end_date.timestamp()
        middle_date = product_start_date + (product_end_date - product_start_date) / 2

        datatakes.sort(
            key=lambda datatake_doc: abs(
                0
                if (
                    datatake_doc.observation_time_start.timestamp()
                    <= middle_date
                    <= datatake_doc.observation_time_stop.timestamp()
                )
                else (
                    middle_date - datatake_doc.observation_time_stop.timestamp()
                    if middle_date > datatake_doc.observation_time_stop.timestamp()
                    else datatake_doc.observation_time_start.timestamp() - middle_date
                )
            )
        )

        nearest_datatake = datatakes[0]

        # ensure the neareset datatake is legit to be THE associated datatake
        if (
            nearest_datatake.observation_time_start.timestamp()
            <= (self.sensing_end_date + tolerance).timestamp()
            and nearest_datatake.observation_time_stop.timestamp()
            >= (self.sensing_start_date - tolerance).timestamp()
        ):
            return nearest_datatake

        return None
