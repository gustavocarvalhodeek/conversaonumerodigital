Conversor de Bases Numéricas e Aritmética Binária

Um aplicativo de desktop completo, construído com Flet (Python), que fornece uma interface gráfica intuitiva para:

Conversão entre diferentes bases numéricas (Binário, Octal, Decimal, Hexadecimal).

Cálculos de aritmética binária (Soma, Subtração, Multiplicação, Divisão).

Visualização do "passo a passo" dos cálculos de conversão.

Captura de Ecrã

Aqui está uma demonstração da interface principal do conversor:

✨ Funcionalidades

Conversor de Bases:

Converte números entre as bases 2 (Binário), 8 (Octal), 10 (Decimal) e 16 (Hexadecimal).

Interface limpa baseada em cartões (Cards) para "Entrada" e "Resultado".

Didático: Mostra um painel com o "passo a passo" do cálculo de conversão (ex: método das divisões sucessivas).

Aritmética Binária:

Realiza operações aritméticas entre dois números binários.

Operações Suportadas: Soma, Subtração, Multiplicação e Divisão (inteira).

Proteção contra divisão por zero.

Exibe o resultado tanto em Binário quanto em Decimal.

Interface (UI/UX):

Interface gráfica moderna construída com Flet.

Design intuitivo usando Cards para separar logicamente as ações.

Menu superior (MenuBar) para acesso às opções "Arquivo" (Sair) e "Ajuda" (Sobre).

Notificações de erro não intrusivas (Banner) para entradas inválidas.

Inicia em modo de tela cheia com rolagem automática para conteúdo extenso.

🚀 Tecnologias Utilizadas

Python 3

Flet: Framework para construir aplicações gráficas (GUI) com Python.

⚙️ Como Executar o Projeto Localmente

Para rodar este projeto na sua máquina, siga os passos abaixo:

1. Clone o Repositório:

git clone [https://github.com/gustavocarvalhodeek/conversaonumerodigital.git](https://github.com/gustavocarvalhodeek/conversaonumerodigital.git)
cd conversaonumerodigital


2. Crie e Ative um Ambiente Virtual (Recomendado):

# Windows
python -m venv .venv
.\.venv\Scripts\activate


3. Instale as Dependências:
O projeto requer apenas a biblioteca flet.

pip install flet


4. Execute o Aplicativo:

python main.py


📦 Como Compilar (Criar o .exe)

Para empacotar o aplicativo em um único executável (.exe), utilize o comando flet pack:

flet pack --onefile --name conversor --add-asset circuito.png main.py


(Se o comando flet não for encontrado, use .\.venv\Scripts\flet.exe ...)

Este projeto foi desenvolvido por Gustavo Carvalho.
