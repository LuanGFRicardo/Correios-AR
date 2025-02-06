import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ExcelUploadForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

def upload_file(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Lê o arquivo Excel
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Converte o DataFrame em uma lista de dicionários
            excel_data = df.to_dict(orient='records')

            # Salva os dados na sessão
            request.session['excel_data'] = excel_data

            # Redireciona para a função de gerar o PDF
            return redirect('gerar_pdf')  # Certifique-se de que a URL 'gerar_pdf' está correta
    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})


def gerar_pdf(request):
    print("Entrou na função gerar_pdf")  # Debug
    if request.method == "GET":
        # Recupera os dados do Excel da sessão
        excel_data = request.session.get('excel_data', [])
        print(f"Dados recuperados da sessão: {excel_data}")  # Debug

        # Se os dados estiverem vazios, retorne uma mensagem de erro
        if not excel_data:
            return HttpResponse("Nenhum dado disponível para gerar o PDF.", status=400)

        # Renderiza o HTML a partir de um template, passando os dados
        html_string = render_to_string('gerarAR.html', {'excel_data': excel_data})
        print("HTML gerado com sucesso")  # Debug

        # Gera o PDF a partir do HTML e define o tamanho da página
        html = HTML(string=html_string)
        pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; margin: 10mm 15mm; }')])  # Ajuste as margens aqui

        print("PDF gerado com sucesso")  # Debug

        # Cria uma resposta HTTP com o PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="documento.pdf"'
        return response
    else:
        return HttpResponse("Método não permitido. Use GET.", status=405)
    
def baixar_excel(request):
    # Define os dados que serão usados para gerar o DataFrame
    dados = [
        # Você pode alterar ou preencher com dados reais conforme necessário
        {
            "remetente_cep": "12345-678",
            "remetente_nome": "Nome Remetente",
            "remetente_endereco": "Endereço Remetente",
            "remetente_numero": "123",
            "remetente_complemento": "Complemento",
            "remetente_bairro": "Bairro",
            "remetente_cidade": "Cidade",
            "remetente_uf": "UF",
            "mao_propria": "Sim",
            "destinatario_cep": "87654-321",
            "destinatario_nome": "Nome Destinatário",
            "destinatario_endereco": "Endereço Destinatário",
            "destinatario_numero": "456",
            "destinatario_complemento": "Complemento",
            "destinatario_bairro": "Bairro",
            "destinatario_cidade": "Cidade",
            "destinatario_uf": "UF",
            "observacao": "Observação",
            "entrega_vizinho": "Não",
        }
        # Adicione mais dicionários conforme necessário
    ]

    # Cria um DataFrame com os dados
    df = pd.DataFrame(dados)

    # Cria a resposta HTTP para o download do arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="dados.xlsx"'

    # Usa o Pandas para escrever o DataFrame no arquivo Excel
    df.to_excel(response, index=False)

    return response