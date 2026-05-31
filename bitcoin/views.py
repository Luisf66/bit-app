import markdown
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

from ai.service.prompt_service import PromptService

from bitcoin.models import TransacaoBTC
from bitcoin.service.dashboard_service import DashboardService
from bitcoin.service.upload_service import BitcoinUploadService, CSVInvalidoError


class TransacaoListView(ListView):
    model = TransacaoBTC
    template_name = 'bitcoin_list.html'
    context_object_name = 'transacoes'

def dashboard_view(request):
    carteira = request.GET.get('carteira', '')
    service = DashboardService()
    context = service.build_context(carteira)

    analise_raw = PromptService().get_or_refresh()
    context['analise_ia'] = markdown.markdown(analise_raw)

    return render(request, 'bitcoin_dashboard.html', context)

def bitcoin_upload_view(request):
    if request.method != 'POST' or not request.FILES.get('arquivo'):
        return render(request, 'bitcoin_upload.html')

    service = BitcoinUploadService(request.FILES['arquivo'])

    try:
        service.validate_csv()
        resultado = service.process_file()
    except CSVInvalidoError as e:
        messages.error(request, str(e))
        return render(request, 'bitcoin_upload.html')
    except RuntimeError as e:
        messages.error(request, str(e))
        return render(request, 'bitcoin_upload.html')

    messages.success(
        request,
        f"Importação concluída: {resultado['transacoes_salvas']} salvas, "
        f"{resultado['transacoes_ignoradas']} ignoradas."
    )
    return redirect('bitcoin:bitcoin-list')