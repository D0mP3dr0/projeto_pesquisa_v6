#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de compilação para proposta de mestrado:
"Modelagem Preditiva de Fluxos Populacionais com Grafos Neurais"

Autor: Luis Felipe Comodo Seelig
Descrição: Este script automatiza o processo de compilação do documento LaTeX,
           oferecendo diversas opções para diferentes etapas do desenvolvimento.
"""

import os
import sys
import argparse
import shutil
import subprocess
from datetime import datetime

# Cores para mensagens no terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Configurações
MAIN_FILE = "main"
OUTPUT_DIR = "output"
LATEX_CMD = "pdflatex"
BIBTEX_CMD = "bibtex"
LATEX_OPTS = f"-interaction=nonstopmode -halt-on-error -output-directory={OUTPUT_DIR}"

def ensure_output_dir():
    """Garante que o diretório de saída exista."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"{Colors.BLUE}Diretório '{OUTPUT_DIR}' criado.{Colors.END}")

def run_command(command, description):
    """Executa um comando com mensagem descritiva."""
    print(f"{Colors.YELLOW}{description}...{Colors.END}")
    try:
        process = subprocess.run(command, shell=True, check=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Erro durante a execução do comando:{Colors.END}")
        print(f"{Colors.RED}{e.stderr}{Colors.END}")
        return False

def compile_full():
    """Compilação completa com processamento de bibliografia."""
    ensure_output_dir()
    
    # Primeira passagem do pdflatex
    if not run_command(f"{LATEX_CMD} {LATEX_OPTS} {MAIN_FILE}", 
                     "Primeira compilação do documento"):
        return False
    
    # Processamento da bibliografia
    os.chdir(OUTPUT_DIR)
    if not run_command(f"{BIBTEX_CMD} {MAIN_FILE}", 
                     "Processando bibliografia"):
        os.chdir("..")
        return False
    os.chdir("..")
    
    # Segunda passagem do pdflatex para incorporar referências
    if not run_command(f"{LATEX_CMD} {LATEX_OPTS} {MAIN_FILE}", 
                     "Segunda compilação para incorporar referências"):
        return False
    
    # Terceira passagem para resolver pendências de referências cruzadas
    if not run_command(f"{LATEX_CMD} {LATEX_OPTS} {MAIN_FILE}", 
                     "Compilação final para resolver referências cruzadas"):
        return False
    
    print(f"{Colors.GREEN}Compilação completa realizada com sucesso!{Colors.END}")
    print(f"{Colors.GREEN}Documento disponível em: {OUTPUT_DIR}/{MAIN_FILE}.pdf{Colors.END}")
    return True

def compile_quick():
    """Compilação rápida sem processar bibliografia."""
    ensure_output_dir()
    
    if run_command(f"{LATEX_CMD} {LATEX_OPTS} {MAIN_FILE}", 
                 "Realizando compilação rápida (sem bibliografia)"):
        print(f"{Colors.GREEN}Compilação rápida concluída com sucesso!{Colors.END}")
        print(f"{Colors.GREEN}Documento disponível em: {OUTPUT_DIR}/{MAIN_FILE}.pdf{Colors.END}")
        return True
    return False

def create_version():
    """Cria versão final para entrega."""
    if not compile_full():
        return False
    
    # Data atual para versionamento
    today = datetime.now().strftime("%Y%m%d")
    version_filename = f"SEELIG_proposta_mestrado_GNN_fluxos_populacionais_{today}.pdf"
    
    # Copia o arquivo compilado para a raiz com nome de entrega
    try:
        shutil.copy(f"{OUTPUT_DIR}/{MAIN_FILE}.pdf", version_filename)
        print(f"{Colors.GREEN}Versão para entrega criada: {version_filename}{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}Erro ao criar versão para entrega: {str(e)}{Colors.END}")
        return False

def clean_temp_files():
    """Remove arquivos temporários de compilação."""
    ensure_output_dir()
    
    extensions = ['.aux', '.log', '.toc', '.lof', '.lot', '.bbl', 
                 '.blg', '.out', '.idx', '.ilg', '.ind']
    
    print(f"{Colors.YELLOW}Removendo arquivos temporários...{Colors.END}")
    count = 0
    for ext in extensions:
        try:
            for file in os.listdir(OUTPUT_DIR):
                if file.endswith(ext):
                    os.remove(os.path.join(OUTPUT_DIR, file))
                    count += 1
        except Exception as e:
            print(f"{Colors.RED}Erro ao remover arquivos {ext}: {str(e)}{Colors.END}")
    
    print(f"{Colors.GREEN}{count} arquivos temporários removidos.{Colors.END}")
    return True

def clean_all():
    """Remove todos os arquivos gerados, incluindo PDFs."""
    clean_temp_files()
    
    print(f"{Colors.YELLOW}Removendo arquivos PDF gerados...{Colors.END}")
    try:
        pdf_path = os.path.join(OUTPUT_DIR, f"{MAIN_FILE}.pdf")
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"{Colors.GREEN}Arquivo PDF removido: {pdf_path}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Erro ao remover PDF: {str(e)}{Colors.END}")
    
    return True

def project_info():
    """Exibe informações sobre o projeto."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}===== Proposta de Mestrado: Modelagem com GNN ====={Colors.END}")
    print(f"{Colors.BOLD}Título:{Colors.END} Modelagem Preditiva de Fluxos Populacionais com Grafos Neurais")
    print(f"{Colors.BOLD}Autor:{Colors.END} Luis Felipe Comodo Seelig")
    print(f"{Colors.BOLD}Estrutura:{Colors.END}")
    print("  - Introdução à pesquisa sobre Grafos Geoespaciais")
    print("  - Revisão da literatura sobre GNN e análise geoespacial")
    print("  - Metodologia de integração de dados espaciais com GNN")
    print("  - Modelagem multimodal: GCN, GAT e TGN")
    print("  - Aplicações em cenários de crise\n")

def main():
    parser = argparse.ArgumentParser(
        description=f'{Colors.BOLD}Compilador da proposta de mestrado sobre Modelagem '
                    f'Preditiva com Grafos Neurais{Colors.END}')
    
    parser.add_argument('-a', '--all', action='store_true',
                        help='Compilação completa com bibliografia')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='Compilação rápida sem bibliografia')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Gera versão final para entrega com data')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Remove arquivos temporários')
    parser.add_argument('-C', '--cleanall', action='store_true',
                        help='Remove todos os arquivos gerados')
    parser.add_argument('-i', '--info', action='store_true',
                        help='Exibe informações sobre o projeto')
    
    args = parser.parse_args()
    
    # Se nenhum argumento fornecido, mostrar ajuda e informações
    if len(sys.argv) == 1:
        project_info()
        parser.print_help()
        return
    
    if args.info:
        project_info()
    
    if args.all:
        compile_full()
    
    if args.quick:
        compile_quick()
    
    if args.version:
        create_version()
    
    if args.clean:
        clean_temp_files()
    
    if args.cleanall:
        clean_all()

if __name__ == "__main__":
    main()