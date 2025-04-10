#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para compilação LaTeX
Busca automaticamente pelo executável pdflatex no sistema
"""

import os
import subprocess
import sys
import glob
from pathlib import Path

def find_pdflatex():
    """Tenta encontrar o executável pdflatex no sistema"""
    possible_paths = [
        # Caminhos comuns do MiKTeX no Windows
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe", 
        r"C:\Program Files (x86)\MiKTeX\miktex\bin\pdflatex.exe",
        # Caminhos comuns do TeX Live no Windows
        r"C:\texlive\2023\bin\win32\pdflatex.exe",
        r"C:\texlive\2022\bin\win32\pdflatex.exe",
        r"C:\texlive\2021\bin\win32\pdflatex.exe",
        # Outros caminhos possíveis
        r"D:\MiKTeX\miktex\bin\x64\pdflatex.exe",
        r"E:\MiKTeX\miktex\bin\x64\pdflatex.exe",
    ]
    
    # Verificar caminhos possíveis
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Encontrado pdflatex em: {path}")
            return path
    
    # Se não encontrou em caminhos específicos, tenta localizar no PATH
    try:
        # No Windows (onde whereis não funciona)
        if os.name == 'nt':
            result = subprocess.run(['where', 'pdflatex'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split('\n')[0]
        else:
            # Em sistemas Unix/Linux
            result = subprocess.run(['which', 'pdflatex'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            if result.returncode == 0:
                return result.stdout.strip()
    except Exception as e:
        print(f"Erro ao procurar pdflatex: {e}")
    
    print("ERRO: Não foi possível encontrar o executável pdflatex.")
    print("Por favor, instale o LaTeX (MiKTeX ou TeX Live) e tente novamente.")
    return None

def compile_document(tex_file, pdflatex_path=None):
    """Compila o documento LaTeX"""
    if not pdflatex_path:
        pdflatex_path = find_pdflatex()
        if not pdflatex_path:
            return False
    
    print(f"\nCompilando {tex_file}...")
    
    # Criar diretório para saída se não existir
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Comando para compilação
    cmd = [
        pdflatex_path,
        "-interaction=nonstopmode",
        "-output-directory=" + output_dir,
        tex_file
    ]
    
    try:
        # Primeira passagem
        print("Primeira passagem...")
        result = subprocess.run(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             text=True)
        
        if "Error" in result.stdout or result.returncode != 0:
            print("ERRO na compilação!")
            print("\nTrechos de erro encontrados:")
            for line in result.stdout.split('\n'):
                if "Error" in line or "!" == line.strip()[0:1]:
                    print(line)
            return False
        
        # Segunda passagem para resolver referências
        print("Segunda passagem...")
        subprocess.run(cmd, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     text=True)
        
        # Verificar se o PDF foi gerado
        pdf_path = os.path.join(output_dir, os.path.splitext(tex_file)[0] + ".pdf")
        if os.path.exists(pdf_path):
            print(f"\nDocumento compilado com sucesso!")
            print(f"PDF gerado em: {pdf_path}")
            
            # Copiar para a raiz para facilitar acesso
            dest_path = os.path.splitext(tex_file)[0] + ".pdf"
            if os.path.exists(pdf_path):
                import shutil
                shutil.copy2(pdf_path, dest_path)
                print(f"Uma cópia do PDF também foi salva em: {dest_path}")
            
            return True
        else:
            print("\nErro: PDF não foi gerado mesmo após compilação aparentemente bem-sucedida.")
            return False
            
    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        return False

def clean_temp_files():
    """Remove arquivos temporários de compilação"""
    extensions = ['.aux', '.log', '.toc', '.lof', '.lot', '.out',
                 '.bbl', '.blg', '.idx', '.ilg', '.ind']
    
    count = 0
    for ext in extensions:
        for file in glob.glob(f"output/*{ext}"):
            try:
                os.remove(file)
                count += 1
            except Exception as e:
                print(f"Erro ao remover {file}: {e}")
    
    print(f"{count} arquivos temporários removidos.")

def main():
    """Função principal"""
    print("==== Compilador LaTeX Simplificado ====")
    
    # Verificar se o arquivo main.tex existe
    if not os.path.exists("main.tex"):
        print("ERRO: Arquivo main.tex não encontrado!")
        return False
    
    # Encontrar o executável do pdflatex
    pdflatex_path = find_pdflatex()
    if not pdflatex_path:
        return False
    
    # Compilar o documento principal
    success = compile_document("main.tex", pdflatex_path)
    
    # Limpar arquivos temporários
    if success:
        clean_temp_files()

    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 