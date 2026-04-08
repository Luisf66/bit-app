import pandas as pd
from django.shortcuts import render

# Create your views here.

def Bitcoin_UploadView(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        df = pd.read_csv(arquivo, sep=',')

        # Exemplo de processamento
        total_comprado = df[df['E/S'] == 'Entrada']['Valor da operacao'].sum()
        total_enviado  = df[df['E/S'] == 'Saida']['Valor da operacao'].sum()
        
        context = {
            'df': df.to_dict('records'),  # lista de dicts para o template
            'total_comprado': total_comprado,
            'total_enviado': total_enviado,
        }

        print(f"Total comprado: {total_comprado}")
        print(f"Total enviado: {total_enviado}")
        print(f"Contexto: {context}")
        return render(request, 'bitcoin_upload.html')
        #return render(request, 'bitcoin_dashboard.html', context)
    
    return render(request, 'bitcoin_upload.html')