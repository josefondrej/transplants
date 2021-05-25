import json

from flask_apispec import MethodResource

from transplants.model.medical_data.blood_type_system.blood_type_codes import all_blood_type_codes


class BloodTypeCodesResource(MethodResource):
    def get(self):
        return dict(
            all_blood_types=json.dumps(all_blood_type_codes)
        )
