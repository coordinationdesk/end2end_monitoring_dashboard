from unittest.mock import patch
from dataclasses import dataclass

import pytest

import maas_cds.model as model

from maas_cds.engines.reports import PublicationConsolidatorEngine

from maas_cds.model.datatake import CdsDatatake
from maas_model import MAASDocument, MAASMessage

# --------------------------------------------------


json_dict = [
    {
        "_index": "raw-data-das-product-2023",
        "_id": "9a6dc7d2872b855a07f7cd8407bdcb3c",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "9827c1ac-655c-4a7a-ad9f-4e66a23edaeb",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QEE_20231214T065148.SAFE",
        "content_length": 92337190,
        "publication_date": "2023-12-14T07:57:38.027Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:15.090Z",
        "modification_date": "2023-12-14T07:57:59.884Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.756Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "d4ba02394e04184fe76495453c1b3999",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "632af865-e10c-4ed6-802c-d71d9840d403",
        "product_name": "S2B_MSIL2A_20231218T121229_N0510_R080_T19CER_20231218T134658.SAFE",
        "content_length": 20065950,
        "publication_date": "2023-12-14T07:58:09.464Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:43.309Z",
        "modification_date": "2023-12-14T07:58:37.872Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.769Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "aad522b6b9fde202688fc99ca37c981d",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "0ee926d7-b578-4fda-9a80-eda86e978061",
        "product_name": "S1A_IW_GRDH_1SDV_20231214T064159_20231214T064224_051647_063C82_63C0_COG.SAFE",
        "content_length": 945152580,
        "publication_date": "2023-12-14T07:56:12.861Z",
        "start_date": "2023-12-14T06:41:59.214Z",
        "end_date": "2023-12-14T06:42:24.213Z",
        "origin_date": "2023-12-14T06:52:09.330Z",
        "modification_date": "2023-12-14T07:56:25.852Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.729Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "c988e2d58b145f529843a26720695e01",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "dfdef2f3-ea6e-45f0-bc1c-16097c6d9e5f",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QCM_20231214T065148.SAFE",
        "content_length": 276007571,
        "publication_date": "2023-12-14T07:59:15.141Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:18.540Z",
        "modification_date": "2023-12-14T07:59:57.222Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.789Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "6d0189bf8ef1edfbe0670176ea804f8f",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "7100ad2e-36ac-4f8b-b71e-98e50d86c641",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QBF_20231214T065148.SAFE",
        "content_length": 289120451,
        "publication_date": "2023-12-14T07:59:47.419Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:16.587Z",
        "modification_date": "2023-12-14T08:00:30.768Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.800Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "5c95a9a1d9e02cb4fbf4960599441195",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "e3166f6e-ce9b-4d8c-a94e-8e4917a1807a",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46REP_20231214T065148.SAFE",
        "content_length": 107003381,
        "publication_date": "2023-12-14T08:00:13.378Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:16.847Z",
        "modification_date": "2023-12-14T08:00:34.528Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.807Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "cc6a20492f27bfa4d576dabdb881752c",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "b92d3fc1-f474-4654-8700-cd1adddb7ea2",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46RCN_20231214T065148.SAFE",
        "content_length": 47616102,
        "publication_date": "2023-12-14T08:00:32.067Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:43.393Z",
        "modification_date": "2023-12-14T08:01:01.620Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.817Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "8dd3b09666fc1050a963e49f6ecf97af",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "a4c5bb2b-1941-47af-bf0f-f4de40a4d14c",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QEJ_20231214T065148.SAFE",
        "content_length": 1173143807,
        "publication_date": "2023-12-14T08:00:50.492Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:24.044Z",
        "modification_date": "2023-12-14T08:02:14.291Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.824Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "ac2a1e99000d7759b67d151dd4df1252",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "ad30bc48-2b37-41d7-a1da-59a4e4469ed6",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QDF_20231214T065148.SAFE",
        "content_length": 773394279,
        "publication_date": "2023-12-14T08:01:12.034Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:36.372Z",
        "modification_date": "2023-12-14T08:02:27.035Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.834Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "9b4afab982e0c9c3a724fc5357efab30",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "27530489-200f-4251-85e0-358f47da321a",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QEF_20231214T065148.SAFE",
        "content_length": 335147902,
        "publication_date": "2023-12-14T07:56:02.158Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:16.670Z",
        "modification_date": "2023-12-14T07:56:36.699Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.726Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "0db667890bf9bd6fc50b2b3331d8fccd",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "77950425-d110-4fc9-b9df-ca182bee0c14",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46RDP_20231214T065148.SAFE",
        "content_length": 240990287,
        "publication_date": "2023-12-14T07:59:39.852Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:18.533Z",
        "modification_date": "2023-12-14T08:00:10.154Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.797Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "6ff0ad3f521d53f259b65dcd57bfa62e",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "3e296746-0846-49f9-b066-0fccaef917d9",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T45QZA_20231214T065148.SAFE",
        "content_length": 119471758,
        "publication_date": "2023-12-14T07:59:48.018Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:17.451Z",
        "modification_date": "2023-12-14T08:00:22.583Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.800Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "8c688274cf4836519b5d12db70e4b28e",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "3b514c7c-36ea-4e0b-a6ad-516bf1858bdf",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QDK_20231214T065148.SAFE",
        "content_length": 1175992684,
        "publication_date": "2023-12-14T08:00:02.532Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:24.286Z",
        "modification_date": "2023-12-14T08:01:23.784Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.805Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "1aa83f994ec0dc9d7d36768574e74ba8",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "7c81180e-83cf-49d2-a0ee-6b9c623b6996",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QCF_20231214T065148.SAFE",
        "content_length": 666067396,
        "publication_date": "2023-12-14T08:00:04.355Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:21.298Z",
        "modification_date": "2023-12-14T08:01:01.372Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.805Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "dac69cb236ec09804368c39ce6231c24",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "598f8825-2252-40cd-ac39-ef1f78b96124",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QCJ_20231214T065148.SAFE",
        "content_length": 738159789,
        "publication_date": "2023-12-14T08:00:32.621Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:21.569Z",
        "modification_date": "2023-12-14T08:01:30.059Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.817Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "40d3f6daadb33d729717e9d918de7234",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "e6b24ee8-a35f-45cd-97ce-0638d1a1b53f",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46REN_20231214T065148.SAFE",
        "content_length": 1162249648,
        "publication_date": "2023-12-14T08:01:31.074Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:39.630Z",
        "modification_date": "2023-12-14T08:02:54.600Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.840Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "c18425703147b60a1cb73829647ca626",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "ed67e730-a7c0-4a41-9efd-24767fb8fadd",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QFH_20231214T065148.SAFE",
        "content_length": 26161648,
        "publication_date": "2023-12-14T07:57:39.073Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:15.915Z",
        "modification_date": "2023-12-14T07:58:08.463Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.756Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "db96b5d061dee7a52bbb6ca70e8bc5d8",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "04c21f86-2773-45a1-a6b9-a70682c28114",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QFK_20231214T065148.SAFE",
        "content_length": 474675060,
        "publication_date": "2023-12-14T07:57:47.855Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:17.490Z",
        "modification_date": "2023-12-14T07:58:27.828Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.760Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "6696a7ec242d298aca4876d0e6dfb336",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "fe975de1-315c-413b-969c-6821b40d0e38",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QFL_20231214T065148.SAFE",
        "content_length": 771693072,
        "publication_date": "2023-12-14T07:59:01.720Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:22.004Z",
        "modification_date": "2023-12-14T08:00:16.455Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.786Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "8b6ea30796d28cc728236a753ee5ed87",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "bcdb2671-5d27-48ff-b024-7bc4fa0889ce",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QDE_20231214T065148.SAFE",
        "content_length": 153299539,
        "publication_date": "2023-12-14T07:59:50.298Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:15.425Z",
        "modification_date": "2023-12-14T08:00:26.667Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.802Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "38a1255d3464e13cc5f6cd066d30a98a",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "11b6bf61-e92b-429b-9154-6bd0e6a1de24",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QCL_20231214T065148.SAFE",
        "content_length": 551955985,
        "publication_date": "2023-12-14T08:00:06.218Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:18.136Z",
        "modification_date": "2023-12-14T08:00:52.043Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.806Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "10e9e213b7251b7c4fe5982fa43850c3",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "e14e18b0-344a-41c7-9996-a78fc7e89d2a",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46RGN_20231214T065148.SAFE",
        "content_length": 55717003,
        "publication_date": "2023-12-14T08:00:14.477Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:16.415Z",
        "modification_date": "2023-12-14T08:00:44.583Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.808Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "ba9aac7172e96fecd7ec5a3b4dfbff0f",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "390dac4a-1891-4c65-af0a-9343b24bb9c9",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QCG_20231214T065148.SAFE",
        "content_length": 752270126,
        "publication_date": "2023-12-14T08:00:20.840Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:36.382Z",
        "modification_date": "2023-12-14T08:01:20.251Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.810Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "c4dd76bac1cfeda3cedd964fcded6e93",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "c6228c1b-c08c-4124-a401-e479cb9d8e0b",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QDM_20231214T065148.SAFE",
        "content_length": 1174491874,
        "publication_date": "2023-12-14T08:01:04.871Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:39.338Z",
        "modification_date": "2023-12-14T08:02:30.327Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.830Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "f94c09503d7cfe10b314f9f8d5ae4e05",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "006e6b78-e354-4804-b183-265bd7c08a65",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QEK_20231214T065148.SAFE",
        "content_length": 1172796416,
        "publication_date": "2023-12-14T08:01:07.245Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:22.276Z",
        "modification_date": "2023-12-14T08:02:29.704Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.831Z",
    },
    {
        "_index": "raw-data-das-product-2023",
        "_id": "0c87b523752a92f7fd48732fc479ee41",
        "reportName": "https://catalogue.dataspace.copernicus.eu",
        "product_id": "6dac54d2-79c8-47b1-bcb1-39574736c890",
        "product_name": "S2A_MSIL2A_20231214T042151_N0510_R090_T46QGM_20231214T065148.SAFE",
        "content_length": 8670908,
        "publication_date": "2023-12-14T08:01:26.401Z",
        "start_date": "2023-12-14T04:21:51.024Z",
        "end_date": "2023-12-14T04:21:51.024Z",
        "origin_date": "2023-12-14T07:43:43.077Z",
        "modification_date": "2023-12-14T08:01:51.545Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
        "ingestionTime": "2023-12-14T08:39:26.838Z",
    },
]

dd_search = []
for jdict in json_dict:
    product = model.DasProduct(**jdict)
    product.meta.id = jdict["_id"]
    product.meta.index = jdict["_index"]

    product.full_clean()

    dd_search.append(product)


# --------------------------------------------------


@pytest.fixture
def datatake_s1():
    datatake_dict = {
        "name": "S1A_MP_ACQ__L0__20231212T172509_20231224T194320.csv",
        "key": "S1A-408706",
        "datatake_id": "408706",
        "hex_datatake_id": "63C82",
        "satellite_unit": "S1A",
        "mission": "S1",
        "observation_time_start": "2023-12-14T06:36:29.627Z",
        "observation_duration": 650952000,
        "observation_time_stop": "2023-12-14T06:47:20.579Z",
        "l0_sensing_duration": 652529000,
        "l0_sensing_time_start": "2023-12-14T06:36:28.836Z",
        "l0_sensing_time_stop": "2023-12-14T06:47:21.365Z",
        "absolute_orbit": "51647",
        "relative_orbit": "125",
        "polarization": "DV",
        "timeliness": "NRT-PT",
        "instrument_mode": "IW",
        "instrument_swath": "0",
        "application_date": "2023-12-12T17:25:09.000Z",
        "updateTime": "2023-12-14T08:25:06.681Z",
    }
    datatake_s1 = CdsDatatake(**datatake_dict)
    datatake_s1.full_clean()
    datatake_s1.meta.id = "S1A-408706-1"
    datatake_s1.meta.index = "cds-datatake-s1-s2"
    return datatake_s1


@pytest.fixture
def datatake_s2():
    datatake_s2_dict = {
        "number_of_expected_tiles": 0,
        "name": "S2A_MP_ACQ__MTL_20231130T120000_20231218T150000.csv",
        "key": "S2A-44274-1",
        "datatake_id": "44274-1",
        "satellite_unit": "S2A",
        "mission": "S2",
        "observation_time_start": "2023-12-14T04:21:52.387Z",
        "observation_duration": 699952000,
        "observation_time_stop": "2023-12-14T04:33:32.339Z",
        "number_of_scenes": 194,
        "absolute_orbit": "44274",
        "relative_orbit": "90",
        "timeliness": "NOMINAL",
        "instrument_mode": "NOBS",
        "application_date": "2023-11-30T12:00:00.000Z",
        "updateTime": "2023-12-14T19:28:23.086Z",
    }
    datatake_s2 = CdsDatatake(**datatake_s2_dict)
    datatake_s2.full_clean()
    datatake_s2.meta.id = "S2A-44274-1"
    datatake_s2.meta.index = "cds-datatake-s1-s2"
    return datatake_s2


@patch(
    "maas_cds.engines.reports.base.BaseProductConsolidatorEngine.get_datatake_dict_S1"
)
@patch(
    "maas_cds.engines.reports.base.BaseProductConsolidatorEngine._get_datatake_S2_map"
)
@patch("maas_engine.engine.RawDataEngine.get_consolidated_documents")
@patch(
    "maas_cds.engines.reports.anomaly_impact.AnomalyImpactMixinEngine._populate_by_CdsPublication"
)
def test_dd_product_consolidation_post_consolidate(
    mock_populate_by_CdsPublication,
    mock_get_consolidated_documents,
    mock_find_datatake_s2,
    mock_find_datatake_s1,
    datatake_s1,
    datatake_s2,
):
    output_doc = []

    for item in dd_search:
        out_m = model.CdsPublication()
        out_m.full_clean()
        out_m.meta.id = item.meta.id
        output_doc.append(out_m)

    mock_get_consolidated_documents.return_value = output_doc

    mock_find_datatake_s1.return_value = {
        "S1A_IW_GRDH_1SDV_20231214T064159_20231214T064224_051647_063C82_63C0_COG": datatake_s1
    }
    mock_find_datatake_s2.return_value = {datatake_s2.meta.id: datatake_s2}

    @dataclass
    class EArgs:
        force = True

    engine = PublicationConsolidatorEngine(args=EArgs(**{}))
    engine.input_documents = dd_search
    engine.payload = MAASMessage(document_class="DasProduct")

    for doc in engine.action_iterator():
        pass

    assert all(doc.datatake_id is not None for doc in engine.consolidated_documents)
    assert len(engine.consolidated_documents) == 26
