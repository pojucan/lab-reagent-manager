# lab-reagent-manager

Uma ferramenta desktop simples e eficiente para gerenciar listas de reagentes laboratoriais utilizando arquivos Excel.

---

## Características

* Busca com autocomplete para reagentes
* Adição rápida de novos registros
* Remoção de entradas incorretas
* Salvamento direto no Excel
* Importação de bases de dados existentes
* Visualização em tabela organizada com rolagem
* Rápido e leve (baseado em Tkinter)

---

## Estrutura do projeto

```
lab-reagent-manager/
│
├── src/
│   └── app.py
│
├── data/input
│   └── sample_reagents.xlsx
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalação

1. Clone o repositório:

```
git clone https://github.com/your-username/lab-reagent-manager.git
```

2. Navegue até a pasta do projeto:

```
cd lab-reagent-manager
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

---

## Uso

Execute a aplicação:

```
python3 src/app.py
```

---

## Como trabalhar

1. Importe um arquivo Excel ou CSV  
2. Adicione ou remova reagentes  
3. Salve as alterações diretamente no mesmo arquivo 

---

## Amostra de arquivo

Um conjunto de dados de exemplo está disponível em:

```
data/input/sample_reagents.xlsx
```

Utilize-o para testar a aplicação.

---

## Dados privados

Os dados originais e notas internas não estão incluídos neste repositório.

Pastas ignoradas:

* `data/` (exceto o arquivo de exemplo)
* `notes/`

---

## Tecnologias

* Python3
* Tkinter
* Pandas

---

## Melhorias futuras

* Prevenção de duplicados  
* Salvamento automático
* Construção de banco de dados com SQLite3 ao invés de Excel

---

## Autor

Pojucan, M.M.S

---

## License

MIT
