import markdown
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from ai.service.prompt_service import PromptService
from bitcoin.models import TransacaoBTC
from bitcoin.service.dashboard_service import DashboardService
from bitcoin.service.upload_service import BitcoinUploadService, CSVInvalidoError


class TransacaoListView(LoginRequiredMixin, ListView):
    model = TransacaoBTC
    template_name = 'bitcoin_list.html'
    context_object_name = 'transacoes'

    def get_queryset(self):
        return TransacaoBTC.objects.filter(usuario=self.request.user)


@login_required
def dashboard_view(request):
    carteira = request.GET.get('carteira', '')
    service = DashboardService(request.user)
    context = service.build_context(carteira)

    prompt_service = PromptService(request.user)
    ultimo = prompt_service.obter_ultimo()

    context['analise_ia'] = markdown.markdown(ultimo.response) if ultimo else None
    context['analise_valida'] = prompt_service.ainda_valido()
    context['analise_data'] = ultimo.created_at if ultimo else None

    return render(request, 'bitcoin_dashboard.html', context)

@login_required
def gerar_analise_view(request):
    if request.method != 'POST':
        return redirect('bitcoin:bitcoin-dashboard')

    prompt_service = PromptService(request.user)

    if prompt_service.ainda_valido():
        messages.warning(request, 'A análise ainda está atualizada.')
        return redirect('bitcoin:bitcoin-dashboard')

    try:
        prompt_service.gerar()
        messages.success(request, 'Análise gerada com sucesso.')
    except Exception as e:
        messages.error(request, f'Erro ao gerar análise: {e}')

    return redirect('bitcoin:bitcoin-dashboard')


@login_required
def bitcoin_upload_view(request):
    if request.method != 'POST' or not request.FILES.get('arquivo'):
        return render(request, 'bitcoin_upload.html')

    service = BitcoinUploadService(request.FILES['arquivo'], request.user)

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