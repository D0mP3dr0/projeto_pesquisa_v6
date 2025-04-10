# Guia de Resolução de Problemas - LaTeX

## Problema Identificado
O sistema está gerando um erro ao tentar compilar seu documento LaTeX. O problema principal é que o compilador `pdflatex` não foi encontrado e o pacote `abntex2` não está instalado.

## Soluções Recomendadas

### 1. Instalar uma Distribuição LaTeX (Recomendado)

Para o Windows, recomendamos instalar o MiKTeX:

1. Acesse https://miktex.org/download
2. Baixe o instalador adequado para o seu sistema
3. Execute o instalador e siga as instruções
4. Após a instalação, abra o "MiKTeX Console" para instalar pacotes adicionais:
   - Vá em "Packages" e pesquise por "abntex2"
   - Selecione o pacote e clique em "+" para instalar

### 2. Modificações feitas no projeto para contornar o problema

Fizemos as seguintes modificações no seu projeto:

- Substituição da classe `abntex2` por `article` (padrão)
- Inclusão de todos os pacotes necessários diretamente no arquivo `main.tex`
- Criação de uma estrutura básica de documento que segue a ABNT sem depender do pacote específico
- Criação de um script Python (`compile_simple.py`) que tenta encontrar automaticamente o pdflatex no seu sistema

### 3. Compilação Online (Alternativa Temporária)

Se a instalação do LaTeX for problemática, você pode usar plataformas online:

1. **Overleaf**: https://www.overleaf.com/
   - Crie uma conta gratuita
   - Faça upload dos seus arquivos 
   - O Overleaf já vem com o abntex2 pré-instalado

2. **LaTeX Base**: https://latexbase.com/

### 4. Verifique o PATH do Sistema

Se você já tem o LaTeX instalado, mas ele não está sendo encontrado:

1. Verifique se os binários do LaTeX estão no PATH do sistema:
   - Abra o PowerShell ou Prompt de Comando
   - Digite `where pdflatex` (Windows) ou `which pdflatex` (Linux/Mac)
   - Se nada for retornado, o executável não está no PATH

2. Adicione os binários do LaTeX ao PATH:
   - Localize a pasta `bin` da sua instalação do LaTeX (normalmente em `C:\Program Files\MiKTeX\miktex\bin\x64\` ou similar)
   - Adicione esta pasta ao PATH do sistema:
     - Windows: Painel de Controle → Sistema → Configurações avançadas do sistema → Variáveis de Ambiente → PATH

### 5. Usando o script simplificado

Após instalar o LaTeX:

1. Volte para o diretório do seu projeto
2. Execute `python compile_simple.py`
3. O script tentará encontrar automaticamente o pdflatex e compilar seu documento

## Para Desenvolvedores da Instituição

Se você estiver compilando este documento em outro ambiente:

1. Instale o pacote abntex2:
   - MiKTeX: Use o MiKTeX Console
   - TeX Live: `tlmgr install abntex2`

2. Restaure as configurações originais:
   - Volte para a classe `abntex2` no arquivo `main.tex`
   - Descomente as linhas de importação de arquivos no preâmbulo
   - Use o script original `compile.py` 