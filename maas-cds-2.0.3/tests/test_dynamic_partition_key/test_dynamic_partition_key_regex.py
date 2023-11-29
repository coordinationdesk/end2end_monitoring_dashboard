from maas_cds.model.dynamic_partition_mixin import DynamicPartitionMixin


class MockProduct(DynamicPartitionMixin):
    def __init__(self, name, product_level):
        self.name = name
        self.product_level = product_level


def test_partitionning():
    product = MockProduct(
        "S1__AUX_WND_V20220404T220000_G20220403T060907.SAFE.zip", "AUX"
    )
    assert product.shall_use_non_sensing_partition_field()

    product = MockProduct(
        "S1B_OPER_MPL_ORBRES_20220401T021300_20220411T021300_0001.EOF.zip", "AUX"
    )
    assert product.shall_use_non_sensing_partition_field()

    product = MockProduct(
        "S3B_DO_0_DOP____20220907T141210_20220907T155144_20220907T161327_5973_070_153______PS2_O_NR_002.SEN3.zip",
        "L0_",
    )
    assert not product.shall_use_non_sensing_partition_field()

    product = MockProduct(
        "S3A_OPER_AUX_POEORB_POD__20220403T071637_V20220308T215942_20220309T235942_DGNS.EOF.zip",
        "___",
    )
    assert product.shall_use_non_sensing_partition_field()
