# servicenow-clone

# Comando para rodar
``python main.py arquivo_original.xml arquivo_clonado.xml --replace "NOME_APLICACAO_ORIGINAL" "NOME_APLICACAO_NOVO" --replace "SCOPE_ORIGINAL" "SCOPE_NOVO" --replace "prefixo_original" "prefixo_novo"``

### Exemplo
``python main.py arquivo_original.xml arquivo_clonado4.xml --replace "Goiás Convergência" "Goiás Encontro de Labs Quatro" --replace "x_sgdg_goias_con_0" "x_1623559_goias_3" --replace "goias_convergencia" "goias_encontro_labs_4"``

# Dependencia
O projeto precisa ter na folder principal o arquivo XML exportado do UPDATE SET da aplicação total.
