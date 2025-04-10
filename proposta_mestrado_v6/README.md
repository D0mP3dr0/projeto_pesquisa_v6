# Proposta de Mestrado - Modelagem Preditiva de Fluxos Populacionais com Grafos Neurais

Este repositório contém a proposta de dissertação de mestrado sobre a modelagem preditiva de fluxos populacionais utilizando Grafos Neurais, com foco em análise retroativa e simulação de movimentos em cenários de crises.

## Estrutura do Projeto

```
proposta_mestrado_v6/
├── bibliografia.bib         # Referências bibliográficas
├── capitulos/               # Capítulos do documento
├── compile.py               # Script original de compilação
├── compile_simple.py        # Script simplificado de compilação
├── main.tex                 # Arquivo principal LaTeX
├── preambulo/               # Arquivos de configuração
└── pre-textuais/            # Elementos pré-textuais
```

## Requisitos

Para compilar este documento, você precisa de:

1. Uma distribuição LaTeX (MiKTeX ou TeX Live)
2. Python 3.x
3. O pacote `abntex2` (para utilizar a versão completa)

## Como Compilar

### Método Simplificado
```bash
python compile_simple.py
```
Este script tenta encontrar o `pdflatex` automaticamente e compilar o documento simplificado.

### Método Original
```bash
python compile.py -a  # Compilação completa com bibliografia
python compile.py -q  # Compilação rápida sem bibliografia
python compile.py -v  # Gera versão para entrega
```

## Resolução de Problemas

Se você encontrar erros durante a compilação, consulte o arquivo `RESOLUCAO_PROBLEMAS.md` para orientações detalhadas.

## Conteúdo da Proposta

Esta proposta de pesquisa aborda:

- Análise de fluxos populacionais usando técnicas de aprendizado de máquina
- Aplicação de Grafos Neurais (GNN) para modelagem espaço-temporal
- Predição de movimentos populacionais em cenários de crises
- Integração de dados geoespaciais com modelos de aprendizado profundo

## Autor

Luis Felipe Comodo Seelig
Instituto Militar de Engenharia 