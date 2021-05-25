import json

from flask_apispec import MethodResource

from transplants.model.medical_data.hla_system.hla_codes import hla_code_groups, all_hla_codes


class HLACodesResource(MethodResource):
    def get(self):
        return dict(
            hla_code_groups=json.dumps(hla_code_groups),
            all_hla_codes=json.dumps(all_hla_codes)
        )