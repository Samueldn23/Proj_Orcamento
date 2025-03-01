# from fpdf import FPDF
#
# def gerar_relatorio(inspecao):
#    pdf = FPDF()
#    pdf.add_page()
#    pdf.set_font("Arial", "B", 12)
#
#    pdf.cell(200, 10, "Relatório de Inspeção SPDA", 0, 1, "C")
#    pdf.cell(200, 10, f"Data: {inspecao.data_inspecao}", 0, 1)
#    pdf.cell(200, 10, f"Técnico: {inspecao.tecnico}", 0, 1)
#    pdf.cell(200, 10, f"Edificação: {inspecao.edificacao.razao_social}", 0, 1)
#
#    pdf.cell(200, 10, "Itens Inspecionados", 0, 1)
#    for item in inspecao.itens:
#        conforme_text = "Conforme" if item.conforme else "Não Conforme"
#        pdf.cell(200, 10, f"{item.descricao}: {conforme_text}", 0, 1)
#
#    pdf.output("relatorio_inspecao.pdf")
#

# Use `gerar_relatorio` após salvar uma inspeção para gerar o PDF
