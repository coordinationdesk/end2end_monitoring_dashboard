"""contains all the model classes"""
# import custom enumeration
from maas_cds.model.enumeration import *

# following import generated DAO classes
from maas_cds.model.generated import *

# import custom DAO implementations

# following import dynamic partition mixin
from maas_cds.model.dynamic_partition_mixin import *

# following import datatake
from maas_cds.model.datatake import *
from maas_cds.model.datatake_s1 import *
from maas_cds.model.datatake_s2 import *

# following import completeness
from maas_cds.model.cds_s3_completeness import *
from maas_cds.model.cds_s5_completeness import *

# following import publication
from maas_cds.model.publication import *

# following import product
from maas_cds.model.product import *
from maas_cds.model.product_s1 import *
from maas_cds.model.product_s2 import *
from maas_cds.model.product_s3 import *
from maas_cds.model.product_s5 import *

# following import dissemination_mixin
from maas_cds.model.dissemination_mixin import *

# following import dd
from maas_cds.model.dd_product import *

# following import das
from maas_cds.model.das_product import *

# following import product type spec
from maas_cds.model.dataflow import *

# following import interface status
from maas_cds.model.interface_status import *

# following import product deletion
from maas_cds.model.product_deletion import *

# consolidated acquisition pass status to feature cams tickets
from maas_cds.model.acquisition_pass_status import *

# HKTM completeness to feature cams tickets
from maas_cds.model.hktm_completeness import *
