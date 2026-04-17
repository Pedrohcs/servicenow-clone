# ServiceNow Application Clone

Uma ferramenta em Python desenvolvida para **clonar aplicações ServiceNow** a partir de um arquivo XML de Update Set, sem afetar ou sobrescrever os recursos do escopo original.

## O Problema Resolvido
Ao tentar duplicar uma aplicação no ServiceNow usando um Update Set e apenas substituindo os nomes/escopos, a plataforma acaba realizando uma **migração** (Update). Isso acontece porque os `sys_id`s dos registros originais são mantidos no XML, fazendo com que o ServiceNow sobrescreva os componentes originais em vez de criar novos.

Este script resolve isso mapeando **todos os `sys_id`s exclusivos** encontrados no arquivo XML e substituindo-os por novos UUIDs gerados dinamicamente. Dessa forma, todos os recursos — incluindo Fluxos (Flow Designer), Tabelas e Interfaces — são clonados de forma totalmente isolada para o novo escopo.

## Pré-requisitos

- **Python 3.6** ou superior instalado na máquina.
- O projeto utiliza apenas bibliotecas nativas do Python (`re`, `uuid`, `argparse`, `pathlib`), portanto, não é necessária a instalação de dependências externas via `pip`.
- O arquivo XML exportado do **Update Set** da aplicação ServiceNow que deseja clonar.

## Como Usar

O script funciona via linha de comando (CLI) e exige um arquivo de entrada (XML original), um arquivo de saída e pelo menos um par de substituição de strings.

### Sintaxe
```bash
python main.py <arquivo_original.xml> <arquivo_clonado.xml> \
  --replace "STRING_ORIGINAL" "NOVA_STRING" \
  --replace "OUTRA_STRING" "OUTRA_NOVA_STRING"
```

**Argumentos Posicionais:**
1. `arquivo_entrada`: Caminho para o arquivo XML exportado do ServiceNow.
2. `arquivo_saida`: Caminho e nome do novo arquivo XML gerado.

**Argumentos Obrigatórios:**
- `--replace`: Recebe dois parâmetros (Valor Antigo e Valor Novo). Pode e deve ser usado múltiplas vezes para substituir o Nome da Aplicação, o Escopo e Prefixos.

## Exemplo Prático

Suponha que você queira clonar a aplicação "Goiás Convergência" para um novo projeto chamado "Goiás Encontro de Labs Quatro". 

Certifique-se de que o arquivo XML (ex: `arquivo_original.xml`) está na pasta raiz do projeto e execute:

```bash
python main.py arquivo_original.xml arquivo_clonado4.xml \
  --replace "Goiás Convergência" "Goiás Encontro de Labs Quatro" \
  --replace "x_sgdg_goias_con_0" "x_1623559_goias_3" \
  --replace "goias_convergencia" "goias_encontro_labs_4"
```

### O que o script fará neste exemplo?
1. Localizará todas as ocorrências de `"Goiás Convergência"`, `"x_sgdg_goias_con_0"` e `"goias_convergencia"` substituindo-as pelos novos valores fornecidos.
2. Fará uma varredura profunda no XML usando Expressões Regulares (`Regex`) para identificar todos os `sys_id`s de 32 caracteres originais.
3. Gerará novos identificadores (`UUIDv4`) para esses recursos.
4. Salvará o resultado em `arquivo_clonado4.xml`.

Por fim, basta importar o `arquivo_clonado4.xml` de volta no ServiceNow e aplicar o Update Set. Uma nova aplicação será instalada, enquanto a antiga permanecerá intacta.

## Avisos e Boas Práticas
* Faça os _replaces_ do nível mais específico (Ex: Nomes de escopo precisos) para o mais generalista.
* Cuidado ao clonar aplicações extremamente grandes; garanta que está passando todos os prefixos que os scripts originais podem utilizar (`x_meu_escopo_antigo` para `x_meu_escopo_novo`).
