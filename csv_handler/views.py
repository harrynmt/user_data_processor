from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import pandas as pd
from .models import UserModel
from .serializers import UserModelSerializer

class CSVUploadView(View):
    def get(self, request):
        return render(request, 'csv_handler/csv_upload.html')  # Render the template when GET request

    def post(self, request):
        csv_file = request.FILES.get('file')

        if not csv_file:
            return render(request, 'csv_handler/csv_upload.html', {'error': 'No file provided.'})

        if not csv_file.name.endswith('.csv'):
            return render(request, 'csv_handler/csv_upload.html', {'error': 'File must have a .csv extension.'})

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return render(request, 'csv_handler/csv_upload.html', {'error': f'Error reading CSV file: {str(e)}'})

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

        return render(request, 'csv_handler/csv_upload.html', {'summary': response_data})
