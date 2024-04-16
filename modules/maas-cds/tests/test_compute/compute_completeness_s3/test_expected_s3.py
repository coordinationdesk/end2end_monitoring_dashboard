from maas_cds.model.cds_s3_completeness import (
    CdsS3Completeness,
)

import pytest


def test_expected_cds_s3_completeness_do_0_nav(cds_s3_completeness_do_0_nav):
    completeness_tolerance = {
        "S3": {
            "local": {
                "DO_0_(DOP|NAV)___|GN_0_GNS___|MW_0_MWR___": -180000000,
                "SL_(0_SLT___|1_RBT___|2_(FRP___|LST___))": -240000000,
                "SR_(0_SRA___|1_SRA_(__|A_|BS))": -540000000,
                "TM_0_(HKM(___|2__)|NAT___)|MW_1_(CAL___|MWR___)": -180000000,
                "OL_(0_EFR___|1_E(FR___|RR___)|2_L(FR___|RR___))": 0,
                "SY_(1_MISR__|2_(AOD___|SYN___|VG(K___|P___)))": 0,
            }
        }
    }

    expected_value = cds_s3_completeness_do_0_nav.get_expected_value()

    assert expected_value == 6060000000

    # Add tolerance to see the diff
    CdsS3Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

    expected_value = cds_s3_completeness_do_0_nav.get_expected_value()

    assert expected_value == 6060000000 - 180000000

    # quick check no residential tolerance in bull action
    datatake_dict_action = cds_s3_completeness_do_0_nav.to_bulk_action()

    assert "COMPLETENESS_TOLERANCE" not in datatake_dict_action["_source"]


def test_expected_cds_s3_completeness_ol_0_efr(cds_s3_completeness_ol_0_efr):

    completeness_tolerance = {
        "S3": {
            "local": {
                "DO_0_(DOP|NAV)___|GN_0_GNS___|MW_0_MWR___": -180000000,
                "SL_(0_SLT___|1_RBT___|2_(FRP___|LST___))": -240000000,
                "SR_(0_SRA___|1_SRA_(__|A_|BS))": -540000000,
                "TM_0_(HKM(___|2__)|NAT___)|MW_1_(CAL___|MWR___)": -180000000,
                "OL_(0_EFR___|1_E(FR___|RR___)|2_L(FR___|RR___))": 0,
                "SY_(1_MISR__|2_(AOD___|SYN___|VG(K___|P___)))": 0,
            }
        }
    }

    expected_value = cds_s3_completeness_ol_0_efr.get_expected_value()

    assert expected_value == 2640000000

    # Add tolerance to see the diff
    CdsS3Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

    expected_value = cds_s3_completeness_ol_0_efr.get_expected_value()

    assert expected_value == 2640000000 + 0

    # Reset completeness tolerance to not impact other test
    CdsS3Completeness.COMPLETENESS_TOLERANCE = {}


def test_expected_sr_0_sra___(cds_s3_completeness_sr_0_sra___):

    completeness_tolerance = {
        "S3": {
            "local": {
                "DO_0_(DOP|NAV)___|GN_0_GNS___|MW_0_MWR___": -180000000,
                "SL_(0_SLT___|1_RBT___|2_(FRP___|LST___))": -240000000,
                "SR_(0_SRA___|1_SRA_(__|A_|BS))": -540000000,
                "TM_0_(HKM(___|2__)|NAT___)|MW_1_(CAL___|MWR___)": -180000000,
                "OL_(0_EFR___|1_E(FR___|RR___)|2_L(FR___|RR___))": 0,
                "SY_(1_MISR__|2_(AOD___|SYN___|VG(K___|P___)))": 0,
            }
        }
    }

    CdsS3Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

    # 92min
    expected_sra = 92 * 60 * 1000 * 1000

    assert expected_sra == cds_s3_completeness_sr_0_sra___.get_expected_value()

    CdsS3Completeness.COMPLETENESS_TOLERANCE = {}
