from maas_cds.engines.operations.missing_consolidation.interface_strategy import (
    AuxipStrategy,
    DdStrategy,
    LtaStrategy,
    PripStrategy,
)


INTERFACE_STRATEGY_DICT = {
    "AUXIP": AuxipStrategy,
    "DD": DdStrategy,
    "PRIP": PripStrategy,
    "LTA": LtaStrategy,
}
