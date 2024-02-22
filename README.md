# aps1-AlgLin

# Projeto: jogo estilo "Angry Birds no espaço"

## Introdução
Esse projeto tem como objetivo a criação de um jogo para aplicar na pratica a manipulação de VETORES, conteudo apreendido na matéria de Algebrá Linear. O projeto foi desenvolvido por Eduardo Takei e Giovanny Russo. O jogo consiste em uma representação de como a força da gravidade age sobre corpos que estão passando por suas proximidades. 

## O Jogo
    Você controlará uma nave espacial, com o objetivo de acertar o astronauta. Determinando a direção e depois atirando, o tiro passa por planetas e pode ter a rota alterada pela gravidade desses planetas.

### Como Jogar
- Setas ↑ e ↓ :
    funcionam para movimentar a nave para cima e para baixo. Possibilitando a procura de um melhor ângulo para o disparo.
- E e Q:
    as teclas E e Q servem para aumentar e diminuir (respectivamente) a velocidade do tiro.
- Barra:
    Aperte BARRA para atirar.
- Direção:
    Use o mouse para direcionar seu disparo, mas ATENÇÃO. O MOUSE deve estar próximo da nave para que o disparo seja possivel.

## Intalação 
Para rodar o jogo, siga os seguintes passos:
### 1. Baixe o Zip
- Nesse link https://github.com/giovannyjvr/aps1-AlgLin, abre a pagina github do projeto, no botão VERDE (Code),  abre a possibilidade de fazer o download por zip de todo o projeto. Portanto:
    ° Botão verde (Code)
    ° Local
    ° HTTPS
    ° Download ZIP

### Descompactando ZIP
- Clique com o botão direito no arquivo.
- Clique em "Extrair Tudo".

### Acessando Jogo
- Clique com botão direito na pasta.
- Clique em "Abrir no Terminal".
#### Instalações necessárias
- execute o seguinte comando :
  pip install -r requirements.txt

#### Jogue
- Execute o seguinte comando para acessar o jogo:
    python jogo.py


## Planetas 
- Cada tela tem um número de planetas com posições fixas
- As imagens dos planetas são aleatórias e não implicam na força da gravidade
### Cálculo da Gravidade

- Para calcular a aceleração da gravidade que os planetas exercem sobre o tiro, foram seguidos os seguintes passos:
    #### 1. Cálculo da Distância entre o Tiro e o Planeta $ \sqrt{(Xplaneta - Xtiro)^2 + (Yplaneta - Ytiro)^2} $
    #### 2. Cálculo da Aceleração Exercida pelo Planeta  $|a| = \frac{c}{d^2}$
    #### 3. Criação de um Vetor Normalizado    $Vetor Normalizado = \frac{Vetor}{np.linalg.norm(vetor)}$
    #### 4. Determinação do Vetor da Aceleração   $Vetor Aceleracão = {|a|}*{Vetor Normalizado}$
    #### 5. Cálculo da Aceleração Resultante $Aceleracao Resultante += Vetor Aceleracão$
    Primeiramente, calculamos a distância entre o tiro e o planeta em questão. Em seguida, calculamos a aceleração que o planeta deve exercer sobre o tiro utilizando $|a| = \frac{c}{d^2}$, onde $c$ é uma constante e $d$ é a distância entre os dois corpos. Para obter a direção da força gravitacional, criamos um vetor através da diferenca entre as coordenadas do planeta e do tiro e assim normalizamos ele para que tenha comprimento igual a 1. Por fim, multiplicamos esse vetor normalizado pela aceleração calculada para criar um vetor com magnitude igual a essa aceleração e então repetimos este cálculo para todos os planetas, resultando em uma aceleração resultante que é aplicada ao tiro
