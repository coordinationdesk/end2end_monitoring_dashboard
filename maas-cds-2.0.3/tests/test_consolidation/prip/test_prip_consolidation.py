from unittest.mock import patch

import pytest

from maas_engine.engine.base import EngineSession

import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
)

from maas_cds.model.datatake import CdsDatatake


@pytest.fixture
def prip_product_s1():
    data_dict = {
        "reportName": "PRIP_S1_Legacy_20220101T000000_20220127T183235_1000_P000000.json",
        "product_id": "44aa2042-edc1-4cbb-b8df-355a53676c96",
        "product_name": "S1A_IW_SLC__1SDV_20211231T222808_20211231T222835_041259_04E753_C3D7.SAFE.zip",
        "content_length": 3850694465,
        "publication_date": "2022-01-01T00:01:02.411Z",
        "start_date": "2021-12-31T22:28:08.622Z",
        "end_date": "2021-12-31T22:28:35.560Z",
        "eviction_date": "2022-01-08T00:01:02.411Z",
        "interface_name": "PRIP_S1_Legacy",
        "production_service_type": "PRIP",
        "production_service_name": "S1-Legacy",
        "ingestionTime": "2022-02-11T14:45:45.713Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "d0fbb9ad9b16c82b50d9445195cf5756"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def prip_product_s2():
    data_dict = {
        "reportName": "https://prip.s2a.atos.copernicus.eu",
        "product_id": "4be1a2aa-9aee-4867-aea4-9799224b4c23",
        "product_name": "S2A_OPER_MSI_L1C_DS_ATOS_20220623T234807_S20220623T220803_N04.00.tar",
        "content_length": 4966400,
        "publication_date": "2022-06-24T00:57:26.305Z",
        "start_date": "2022-06-23T22:08:03.000Z",
        "end_date": "2022-06-23T22:09:40.000Z",
        "origin_date": "2022-06-23T23:33:50.655Z",
        "footprint": "geography'SRID=4326;POLYGON((-55.4396709485611 79.2367901656332,-55.4392803167965 79.2369161105538,-55.4413671048159 79.2371271249615,-55.4408752047734 79.2372852982615,-55.4411098096461 79.2373095662594,-55.4406471943289 79.237458189023,-55.4416038674767 79.2375560357813,-55.4413478208163 79.2376382203227,-55.4418088781096 79.2376850767256,-55.4408960942972 79.2379775764714,-55.4413018077367 79.2380192167156,-55.4410114711817 79.2381121699677,-55.4412088383559 79.2381322668209,-55.4407115484121 79.2382913295728,-55.442419851691 79.2384659083884,-55.4206666045729 79.2452186645181,-54.8008292793751 79.4366861976227,-54.7946142440176 79.4360496369524,-54.7891688118177 79.4377194601513,-54.7867645266574 79.4374696279815,-54.2108830117573 79.6141240500475,-54.2118512761637 79.6142251216694,-54.21178307625 79.6142460330039,-54.2171123910689 79.6147927189794,-54.216701902627 79.6149182041642,-54.2171664920613 79.6149665611921,-54.2170887888653 79.6149903049411,-54.2179391889926 79.6150781482347,-54.2176710017492 79.6151600625272,-54.2187525515272 79.6152721906933,-53.7594103398381 79.751682392571,-53.56310660016 79.8099626967281,-53.5553391557403 79.8091551818514,-53.5544946720777 79.8094009761958,-53.5522181136261 79.8091635454334,-53.5469256531781 79.8107042377392,-53.54611418322 79.8106203430551,-52.9487087653301 79.9844693715272,-52.9510660212611 79.9847148726847,-52.9508370487141 79.9847815133501,-52.9592626876181 79.9856740103128,-52.2794228259424 80.1791751997514,-52.2704184563098 80.1782224000389,-52.2630392573614 80.1802585075581,-52.2622714066569 80.180177959434,-52.261879541882 80.180285859203,-52.2584655579714 80.1799216752917,-51.6275110729182 80.3535962038288,-51.6398780950449 80.3549263271519,-51.3081395375992 80.4451922663457,-50.9223449170281 80.5497539576026,-50.9117694055481 80.5486195532291,-50.9019049085099 80.5511894087498,-50.9005981354969 80.5510503637244,-50.8998324958838 80.5512487583509,-50.8988274793245 80.5511399092933,-50.2176381294426 80.7274946862215,-50.2306146873322 80.7289178262026,-49.6290987122625 80.8845856767472,-49.6128000178199 80.8887737413658,-49.4571243417442 80.9285913179217,-49.4431577771816 80.9270590516768,-49.3010986838163 80.9617963113009,-48.6673799037687 81.1155920942838,-48.6600886092979 81.1173591790342,-48.5464735951471 81.1047996759419,-47.767494549357 81.0168256227483,-47.0036411750198 80.9272699121794,-46.2542922928814 80.836161364378,-45.5189224532593 80.7437142251507,-44.7983987875646 80.6497729020808,-44.0904495684565 80.554863215681,-43.3970077396479 80.4584149234941,-42.7166754585919 80.3607658636523,-42.0502058974636 80.2617468459522,-41.3963558982465 80.1615105073957,-40.7550032037776 80.0601592051876,-40.1266389285253 79.9575963435295,-39.5103260950619 79.8539823216352,-38.9063408305639 79.7492235353559,-38.3144261439374 79.6433654723212,-37.7341341934676 79.5364567094815,-37.1651339387886 79.4285673424268,-36.6072980178184 79.3197362531057,-36.0600454187869 79.2101179812324,-35.5232212529977 79.0997110135622,-34.9969722212544 78.9884270519118,-34.4811059431672 78.8761619439892,-33.9749434789713 78.7630915403117,-33.4783592208928 78.649267679316,-32.9916646166796 78.5346241603116,-32.5144823648319 78.4191864395012,-32.0460205545409 78.3030280698624,-31.5868347805674 78.1860920314975,-31.1364020308076 78.0684370363697,-30.6942651063542 77.9501404447224,-30.2601850446289 77.831278745751,-29.8340534066119 77.7119135746523,-29.4157911466266 77.5919582035509,-29.0056041981455 77.4712871925297,-28.6035152880245 77.349903262062,-28.2075625321507 77.2281160330722,-27.8212416873048 77.1065605145441,-28.2155960922355 77.0375270445014,-28.3541950749156 77.013324954739,-28.6647142006903 76.9596339913642,-28.6654192829089 76.959852321433,-28.6659353660655 76.9597591224951,-28.6696799921645 76.9609173575763,-29.3939720467897 76.8291642440141,-29.3935096400945 76.8290236769739,-29.4004712235918 76.82776399102,-29.399782813946 76.8275547108347,-29.4008953025542 76.8273523542152,-29.3986335651055 76.8266655021834,-29.5803355244197 76.7935105168888,-29.9297343267307 76.7298605939455,-29.9728135458093 76.7220372771339,-29.9968945672893 76.717667772603,-30.1876646998484 76.6830918109775,-30.1918917123038 76.6843540151216,-30.1922908053697 76.6842789542259,-30.1925769134009 76.6843645961942,-30.8782547958883 76.5553239238712,-30.8776126776833 76.5551345213096,-30.8845489012177 76.5538306459201,-30.8842064786054 76.553729950696,-30.8844608116284 76.5536822130723,-30.8823435743564 76.5530582654995,-30.9286955437011 76.5442753523612,-31.0988820831674 76.5120760932613,-31.6349403534381 76.4107864848568,-31.6382055418205 76.4117317383423,-31.6386610385767 76.4116434955937,-31.6387706790804 76.4116753132367,-32.3002868313522 76.2834959550468,-32.3002326112636 76.2834804380745,-32.306465876258 76.2822726597164,-32.3062188350842 76.2822021658905,-32.3062798102481 76.2821903623825,-32.305554010354 76.2819830479478,-32.3059308964781 76.281910055939,-32.3043739034958 76.281464853009,-33.0336703079031 76.1380613823502,-33.0363086577717 76.13880337596,-33.6850816708604 76.0094841140031,-33.6850040864299 76.0094625794553,-33.6853715633195 76.0093893469983,-33.6849051439779 76.0092595760648,-33.6904503524951 76.0081536245061,-33.690147937424 76.0080697421348,-33.6907545214074 76.0079486239671,-33.6904211826264 76.0078560736913,-33.6905033234478 76.0078396831994,-33.6896331417983 76.0075977787507,-34.4078246227077 75.8608678581744,-34.410114493723 75.8614942794511,-34.4104075967177 75.8614342299704,-34.4106406067938 75.8614981259865,-34.4117786107743 75.8612651736345,-34.4117926506088 75.8612690139478,-34.4358262077449 75.8563425684666,-35.057333588917 75.7291184034014,-35.0566239195 75.728926232656,-35.062494242754 75.7277222896722,-35.0617883818576 75.7275318093516,-35.7807518922727 75.5750053341721,-35.782531309641 75.5754792093108,-35.782647348852 75.5754547795402,-35.7832354218712 75.5756117494505,-35.7902454176997 75.5741375889347,-35.7910841752995 75.5743609074697,-36.0276188981102 75.5242193549053,-36.4909750648933 75.4267783032241,-36.9000445645705 75.5344903403977,-37.320589903669 75.6428735574144,-37.7471339102852 75.7505955842732,-38.1805201588024 75.8574340272184,-38.6200753200058 75.963480600509,-39.0657477353303 76.068746000484,-39.5182875525779 76.1731146805995,-39.9768004009513 76.2769090108897,-40.4421283575199 76.3799278132133,-40.9142609411384 76.4821808810904,-41.3933406844822 76.5835039138455,-41.8793185754927 76.6839592494725,-42.3727724231155 76.7833451781338,-42.8734374580038 76.881785888961,-43.3808997870789 76.9793780133475,-43.8958458521121 77.0760287389586,-44.4185581489988 77.1715928687764,-44.9486628921318 77.2660942956104,-45.4863826145742 77.3594900405538,-46.0318102119059 77.451861259018,-46.5849844015768 77.5432859293737,-47.1461586885172 77.6336374845143,-47.7153842833254 77.722863403993,-48.2923264578048 77.8109915842278,-48.877551256284 77.8978285729504,-49.4709295038228 77.9834249126328,-50.0724080154597 78.067844555816,-50.6821355974974 78.1509810120421,-51.3002540953466 78.2328544974366,-51.9269277283676 78.3133304047979,-52.5616746603038 78.3924026277712,-53.204909230181 78.4700830808615,-53.856652031394 78.5463699138219,-54.516866699033 78.6211350876412,-55.1854219007176 78.6946467604886,-55.8621563252805 78.7668710251172,-56.5477862153468 78.8373766631626,-56.6553262885438 78.8481921651582,-56.5515522412022 78.8818392877757,-56.0162552948632 79.0535556992835,-56.0112990146124 79.0530565464896,-56.0068180886139 79.0545005682974,-56.0038680505514 79.0541974401884,-55.4859422019517 79.2213357520929,-55.4402732866645 79.2359628210907,-55.4405337212605 79.2359893879935,-55.4384441917522 79.2366636938534,-55.4396709485611 79.2367901656332))'",
        "interface_name": "PRIP_S2A_ATOS",
        "production_service_type": "PRIP",
        "production_service_name": "S2A-ATOS",
        "ingestionTime": "2022-06-24T01:19:43.881Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "c50037db4a36d66d47246fdf524fd149"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def prip_product_s3():
    data_dict = {
        "reportName": "PRIP_S3_Legacy_20220101T000000_20220127T184737_1000_P000023.json",
        "product_id": "71700e9a-bb3f-3778-8960-63e165e70aba",
        "product_name": "S3A_SY_2_VG1____20220121T000000_20220121T235959_20220122T204333_NORTH_AMERICA_____LN2_O_ST_002.SEN3.zip",
        "content_length": 35160306,
        "publication_date": "2022-01-22T21:41:49.332Z",
        "start_date": "2022-01-21T00:00:00.000Z",
        "end_date": "2022-01-21T23:59:59.000Z",
        "eviction_date": "2022-01-29T21:41:49.332Z",
        "interface_name": "PRIP_S3_Legacy",
        "production_service_type": "PRIP",
        "production_service_name": "S3-Legacy",
        "ingestionTime": "2022-02-11T08:51:14.175Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "d0fbb9ad9b16c82b50d9445195cf5756"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_product_consolidation(mock_mget_by_ids, prip_product_s1, dd_attrs):
    datatake_doc = CdsDatatake()

    datatake_doc.datatake_id = "321363"
    datatake_doc.absolute_orbit = "41259"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    engine.session = EngineSession()

    product = engine.consolidate_from_PripProduct(prip_product_s1, model.CdsProduct())

    engine.consolidated_documents = [product]

    engine.on_post_consolidate()

    product.full_clean()

    assert product.to_dict() == {
        "absolute_orbit": "41259",
        "datatake_id": "321363",
        "instrument_mode": "IW",
        "content_length": 3850694465,
        "key": "de080dea60537a05416bc10a8139e154",
        "mission": "S1",
        "name": "S1A_IW_SLC__1SDV_20211231T222808_20211231T222835_041259_04E753_C3D7.SAFE.zip",
        "polarization": "DV",
        "prip_id": "44aa2042-edc1-4cbb-b8df-355a53676c96",
        "prip_publication_date": "2022-01-01T00:01:02.411Z",
        "prip_service": "PRIP_S1_Legacy",
        "product_level": "L1_",
        "product_class": "S",
        "product_type": "IW_SLC__1S",
        "satellite_unit": "S1A",
        "sensing_start_date": "2021-12-31T22:28:08.622Z",
        "sensing_end_date": "2021-12-31T22:28:35.560Z",
        "sensing_duration": 26938000.0,
        "timeliness": "NTC",
    }


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation(mock_mget_by_ids, prip_product_s1):
    datatake_doc = CdsDatatake()

    datatake_doc.datatake_id = "321363"
    datatake_doc.absolute_orbit = "41259"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s1, model.CdsPublication()
    )

    publication.full_clean()

    engine.mfill_timeliness_S1([publication])

    assert publication.to_dict() == {
        "absolute_orbit": "41259",
        "content_length": 3850694465,
        "datatake_id": "321363",
        "eviction_date": "2022-01-08T00:01:02.411Z",
        "from_sensing_timeliness": 5546851000.0,
        "instrument_mode": "IW",
        "key": "d0fbb9ad9b16c82b50d9445195cf5756",
        "mission": "S1",
        "name": "S1A_IW_SLC__1SDV_20211231T222808_20211231T222835_041259_04E753_C3D7.SAFE.zip",
        "polarization": "DV",
        "product_level": "L1_",
        "product_class": "S",
        "product_type": "IW_SLC__1S",
        "product_uuid": "44aa2042-edc1-4cbb-b8df-355a53676c96",
        "publication_date": "2022-01-01T00:01:02.411Z",
        "satellite_unit": "S1A",
        "sensing_start_date": "2021-12-31T22:28:08.622Z",
        "sensing_end_date": "2021-12-31T22:28:35.560Z",
        "sensing_duration": 26938000.0,
        "service_id": "S1-Legacy",
        "service_type": "PRIP",
        "timeliness": "NTC",
    }


@patch("maas_cds.model.CdsDatatake.get_by_id")
def test_prip_publication_consolidation_s3(mock_get_by_id, prip_product_s3):
    datatake_doc = CdsDatatake()

    datatake_doc.datatake_id = "321363"
    datatake_doc.absolute_orbit = "41259"

    mock_get_by_id.return_value = datatake_doc

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s3, model.CdsPublication()
    )

    publication.full_clean()

    assert publication.to_dict() == {
        "key": "d0fbb9ad9b16c82b50d9445195cf5756",
        "mission": "S3",
        "name": "S3A_SY_2_VG1____20220121T000000_20220121T235959_20220122T204333_NORTH_AMERICA_____LN2_O_ST_002.SEN3.zip",
        "product_level": "L2_",
        "product_type": "SY_2_VG1___",
        "satellite_unit": "S3A",
        "timeliness": "ST",
        "sensing_start_date": "2022-01-21T00:00:00.000Z",
        "sensing_end_date": "2022-01-21T23:59:59.000Z",
        "sensing_duration": 86399000000,
        "content_length": 35160306,
        "service_id": "S3-Legacy",
        "service_type": "PRIP",
        "product_uuid": "71700e9a-bb3f-3778-8960-63e165e70aba",
        "publication_date": "2022-01-22T21:41:49.332Z",
        "eviction_date": "2022-01-29T21:41:49.332Z",
        "from_sensing_timeliness": 78110332000,
    }


@patch("maas_cds.model.CdsDatatake.get_by_id", return_value=None)
def test_action(mock_get_by_id, prip_product_s1, dd_attrs):
    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    product = engine.consolidate_from_PripProduct(prip_product_s1, model.CdsProduct())

    assert engine.get_report_action("created", product) == "new.cds-product-s1"


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation(mock_mget_by_ids, prip_product_s3):
    datatake_doc = CdsDatatake()

    datatake_doc.datatake_id = "326613"
    datatake_doc.absolute_orbit = "41864"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s3, model.CdsPublication()
    )

    publication.full_clean()

    expected_dict = {
        "content_length": 35160306,
        "eviction_date": "2022-01-29T21:41:49.332Z",
        "from_sensing_timeliness": 78110332000,
        "key": "d0fbb9ad9b16c82b50d9445195cf5756",
        "mission": "S3",
        "name": "S3A_SY_2_VG1____20220121T000000_20220121T235959_20220122T204333_NORTH_AMERICA_____LN2_O_ST_002.SEN3.zip",
        "product_level": "L2_",
        "product_type": "SY_2_VG1___",
        "product_uuid": "71700e9a-bb3f-3778-8960-63e165e70aba",
        "publication_date": "2022-01-22T21:41:49.332Z",
        "satellite_unit": "S3A",
        "sensing_duration": 86399000000,
        "sensing_end_date": "2022-01-21T23:59:59.000Z",
        "sensing_start_date": "2022-01-21T00:00:00.000Z",
        "service_id": "S3-Legacy",
        "service_type": "PRIP",
        "timeliness": "ST",
    }

    assert publication.to_dict() == expected_dict


@patch("maas_cds.model.s2_tilpar_tiles.S2Tiles.intersection")
# @patch("maas_cds.lib.queryutils.find_datatake_from_sensing.find_datatake_from_sensing")
@patch("opensearchpy.MultiSearch.execute")
def test_prip_footprint_consolidation(
    mock_find_mget_by_ids, mock_tiles_intersection, prip_product_s2, dd_attrs
):
    # maas_migrate -r maas-cds/resources/ --es-url=http://localhost:9200 --es-username=admin --es-password=admin -v --populate s2-tilpar-tiles.bulk.xz

    datatake = {
        "name": "S2A_MP_ACQ__MTL_20220616T120000_20220704T150000.csv",
        "key": "S2A-36577-1",
        "datatake_id": "36577-1",
        "satellite_unit": "S2A",
        "mission": "S2",
        "observation_time_start": "2022-06-23T22:07:45.505Z",
        "observation_duration": 101024000,
        "observation_time_stop": "2022-06-23T22:09:26.529Z",
        "number_of_scenes": 28,
        "absolute_orbit": "36577",
        "relative_orbit": "115",
        "timeliness": "NOMINAL",
        "instrument_mode": "NOBS",
        "application_date": "2022-06-16T12:00:00.000Z",
        "updateTime": "2022-06-24T02:20:05.659Z",
    }

    datatake_doc = CdsDatatake(**datatake)
    datatake_doc.full_clean()
    datatake_doc.meta.id = datatake_doc.key

    mock_find_mget_by_ids.return_value = [[datatake_doc]]

    mock_tiles_intersection.return_value = [
        "24XVP",
        "24XVQ",
        "24XWM",
        "24XWP",
        "23XNE",
        "23XNH",
        "23XNK",
        "26XMM",
        "25XDD",
        "25XDE",
    ]

    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    engine.session = EngineSession()

    product = engine.consolidate_from_PripProduct(prip_product_s2, model.CdsProductS2())

    engine.consolidated_documents = [product]

    engine.on_post_consolidate()

    product.full_clean()

    expected_dict = {
        "absolute_orbit": "36577",
        "datatake_id": "36577-1",
        "key": "aededde8b5433c159358ed55363ed5aa",
        "instrument_mode": "NOBS",
        "mission": "S2",
        "name": "S2A_OPER_MSI_L1C_DS_ATOS_20220623T234807_S20220623T220803_N04.00.tar",
        "product_level": "L1_",
        "product_type": "MSI_L1C_DS",
        "satellite_unit": "S2A",
        "site_center": "ATOS",
        "sensing_start_date": "2022-06-23T22:08:03.000Z",
        "sensing_end_date": "2022-06-23T22:09:40.000Z",
        "sensing_duration": 97000000,
        "content_length": 4966400,
        "timeliness": "NOMINAL",
        "prip_id": "4be1a2aa-9aee-4867-aea4-9799224b4c23",
        "prip_publication_date": "2022-06-24T00:57:26.305Z",
        "prip_service": "PRIP_S2A_ATOS",
        "expected_tiles": [
            "24XVP",
            "24XVQ",
            "24XWM",
            "24XWP",
            "23XNE",
            "23XNH",
            "23XNK",
            "26XMM",
            "25XDD",
            "25XDE",
        ],
    }

    assert product.to_dict() == expected_dict


@patch("opensearchpy.Search.execute", return_value=[])
def test_prip_contained_product_consolidation(
    mock_es_search_execute, s2_raw_l2a_tc, dd_attrs
):
    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    product = engine.consolidate_from_PripProduct(s2_raw_l2a_tc, model.CdsProduct())

    product.full_clean()

    expected_dict = {
        "absolute_orbit": "36312",
        "key": "00000498248b6695705f2c8f7e8ab372",
        "mission": "S2",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20220605T110112_A036312_T43XDG_N04.00.jp2",
        "prip_id": "1d3c9b81-990b-44a0-b306-3ef104896de8",
        "prip_publication_date": "2022-06-05T11:45:37.934Z",
        "prip_service": "PRIP_S2A_ATOS",
        "product_discriminator_date": "2022-06-05T11:01:12.000Z",
        "product_level": "L2_",
        "product_type": "MSI_L2A_TC",
        "satellite_unit": "S2A",
        "sensing_duration": 202000000,
        "content_length": 93419,
        "sensing_end_date": "2022-06-05T09:29:19.000Z",
        "sensing_start_date": "2022-06-05T09:25:57.000Z",
        "site_center": "ATOS",
        "tile_number": "43XDG",
        "timeliness": "_",
    }

    assert product.to_dict() == expected_dict
