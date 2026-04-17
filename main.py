import re
import uuid
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def clonar_update_set(conteudo_xml, substituicoes):
    """
    Clona uma aplicação de um Update Set substituindo sys_ids e um conjunto de strings.

    Args:
        conteudo_xml (str): O conteúdo XML do Update Set original.
        substituicoes (list): Uma lista de tuplas, onde cada tupla contém (string_antiga, string_nova).

    Returns:
        str: O conteúdo XML modificado com a aplicação clonada.
    """
    # Mapa para todas as substituições
    mapa_substituicao = {}

    # 1. Mapear as substituições de strings personalizadas
    print("Mapeando strings para substituição...")
    for antigo, novo in substituicoes:
        mapa_substituicao[antigo] = novo
        print(f"  - Mapeando '{antigo}' -> '{novo}'")

    # 2. Encontrar todos os sys_ids únicos e mapeá-los para novos UUIDs
    print("\nMapeando sys_ids para clonagem...")
    padrao_sys_id = re.compile(r'[a-f0-9]{32}')
    sys_ids_encontrados = set(padrao_sys_id.findall(conteudo_xml))
    
    print(f"Encontrados {len(sys_ids_encontrados)} sys_ids únicos para mapear.")
    for id_antigo in sys_ids_encontrados:
        # Garante que não vamos substituir algo que já está no mapa de nomes/escopos
        if id_antigo not in mapa_substituicao:
            mapa_substituicao[id_antigo] = uuid.uuid4().hex

    # 3. Criar uma única expressão regular para todas as chaves a serem substituídas.
    # Ordenar as chaves pelo comprimento (do maior para o menor) para evitar
    # substituições parciais incorretas (ex: substituir "foo" dentro de "foobar").
    chaves_ordenadas = sorted(mapa_substituicao.keys(), key=len, reverse=True)
    regex_substituicao = re.compile("|".join(map(re.escape, chaves_ordenadas)))

    # 4. Definir a função que fará a substituição com base no mapa
    def get_replacement(match):
        return mapa_substituicao[match.group(0)]

    # 5. Executar a substituição em uma única passagem
    print("\nExecutando substituições no conteúdo XML...")
    conteudo_clonado = regex_substituicao.sub(get_replacement, conteudo_xml)
    
    return conteudo_clonado


def main():
    """
    Função principal para executar o script a partir da linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Clona uma aplicação em um Update Set do ServiceNow, alterando sys_ids e strings personalizadas."
    )
    parser.add_argument("arquivo_entrada", type=Path, help="Caminho para o arquivo XML original.")
    parser.add_argument("arquivo_saida", type=Path, help="Caminho para salvar o novo arquivo XML atualizado.")
    
    parser.add_argument(
        '--replace',
        nargs=2,
        metavar=('ANTIGO', 'NOVO'),
        action='append',
        required=True,
        help="Define um par de strings para substituição (ex: --replace 'original' 'novo'). Pode ser usado várias vezes."
    )

    args = parser.parse_args()

    try:
        print(f"Lendo o arquivo: {args.arquivo_entrada}")
        with open(args.arquivo_entrada, 'r', encoding='utf-8') as f_in:
            xml_original = f_in.read()

        xml_clonado = clonar_update_set(
            xml_original, args.replace
        )

        print(f"Salvando o arquivo atualizado em: {args.arquivo_saida}")
        with open(args.arquivo_saida, 'w', encoding='utf-8') as f_out:
            f_out.write(xml_clonado)
        
        print("\nProcesso de clonagem concluído com sucesso!")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{args.arquivo_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()