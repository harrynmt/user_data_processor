from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .serializers import UserModelSerializer
from .models import UserModel

class CSVUploadView(APIView):

    def post(self, request):
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must have a .csv extension."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({"error": f"Error reading CSV file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        saved_count = 0
        rejected_records = []

        for index, row in df.iterrows():
            data = {
                'name': row.get('name'),
                'email': row.get('email'),
                'age': row.get('age')
            }

            serializer = UserModelSerializer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved_count += 1
                except Exception as e:
                    rejected_records.append({'row': index + 2, 'error': str(e)})
            else:
                rejected_records.append({'row': index + 2, 'errors': serializer.errors})

        response_data = {
            'total_saved': saved_count,
            'total_rejected': len(rejected_records),
            'rejected_records': rejected_records,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
