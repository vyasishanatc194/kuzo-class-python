from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from core.api.serializers import EventScriptSerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# contact us API
# .................................................................................


class ScriptCreateAPI(MyAPIView):

    """API View to create contact us"""

    permission_classes = (AllowAny,)
    serializer_class = EventScriptSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data,  context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "OK", "message": "Successfully submitted details", "data": serializer.data})

        else:
            return Response({"status": "FAIL", "message": "Cannot submit script", "data": serializer.errors})

       