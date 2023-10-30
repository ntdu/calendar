# -*- coding: utf-8 -*-
import json
from datetime import datetime


def get_health_check_view(service_name: str, service_port: int):
    from rest_framework.response import Response
    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import AllowAny
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def api_health_check_view(request):
        return Response(
            json.dumps({
                "status": "running",
                "info": {
                    "name": service_name,
                    "port": service_port,
                    "code": "python-django",
                },
                "date": datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
                #  "2022-10-18T04:40:40.207Z"
            }), status=200
        )
    return api_health_check_view