# Yes or No Automatic Checklist
yorn surgiu enquanto eu estava respondendo uma checklist manualmente para saber se estava pronto para entrar em um relacionamento. Pensei: "eu bem que podia automatizar isso", então nasceu meu primeiro projeto.

#### Clone o repositório.
```bash
# clone o repositório
git clone https://github.com/CAPTURACERTA/YorN_checklist.git

# acesse o diretório do projeto
cd YorN_checklist
```
#
---

# Documentação

### O que é yorn?
De forma simples: yorn é um leitor de arquivo txt.

Ele espera alguns parâmetros globais seguidos de perguntas encapsuladas pela sintaxe do programa e desenha um resultado em outro arquivo com feedback de sucesso ou fracasso. Ou seja, seu objetivo primordial é ser um programa de checklist objetiva que lê perguntas, coleta as respostas do usuário e envia um feedback de acordo com as respostas.

### Conhecendo o yorn
---
#### -executando o programa
O arquivo principal `main.py` espera 2 argumentos, o arquivo a ser lido, contendo as perguntas, e o a ser escrito. 

Ex: `python main.py your_file1.txt your_file2.txt`

Se o arquivo a ser lido não existir, ou só um argumento for dado, ou mais de dois, ou se algum dos arquivos não estiverem em formato txt, o programa enviará uma menssagem de erro por terminal e encerrará. Se o arquivo a ser escrito `your_file2.txt` já existir, o programa perguntará se o usuário tem certeza se quer substituí-lo.

Ou seja, o arquivo a ser lido deve existir. O a ser escrito pode ou não exisitr.

#### -como escrever em yorn
Como dito antes, yorn é um leitor de texto que visa automatizar a criação e resposta de uma checklist objetiva.
>Com "objetiva", quero dizer que a estrutura da checklist funciona de forma que um resultado final é esperado. Ex: um processo seletivo. Cada competência exigida tem um peso diferente, logo um candidato pode passar ou não dependendo das competências que atende.

Assim, compreende-se que você escreverá em um arquivo txt e o programa interpretará o texto. Como uma linguagem de marcação.

Explicado isso, tomemos como exemplo o seguinte e-mail:
![image](https://github.com/user-attachments/assets/40116b16-16f6-4a9f-acb8-8b0cddf139c7)
No 2° parágrafo, o escritor faz algumas perguntas para saber se Bob seria capaz de prosseguir com o projeto. Essas perguntas são o nosso objetivo. Eis a sintaxe, caso quisessemos capturá-las:
```
>Consegue entregar uma versão básica de teste ainda nesse mês? {9};
>Consegue diminuir os custos? {5,s};
>Consegue mudar o nome do projeto para o nome do diretor geral?;
```
#### -perguntas
Isso que você acabou de ler é a forma como o programa interpreta perguntas. Vamos dismiuçá-las:

`->` A seta demarca o começo de uma pergunta. Ela pode ser apenas um ">", ou vários "-" seguido de um ">". Regex: "-*>".

`texto` Após a seta, entra o texto da pergunta. "---->Consegue diminuir os custos?"

`{pontos,comentário?}` Após o texto, entra os parâmetros, quantos pontos a pergunta vale e se ela admite comentário. Os parâmetros são opcionais, se você não os providênciar eles terão seus valores padrões: "{1,n}", que significa um ponto e sem comentário. Você pode colocar apenas um parâmetro, "{s}" ou "{2}", mas, caso ponha os dois, o ponto deve vir primeiro. Além disso, os pontos só vão até nove. Caso ponha um valor >= 10, desrespeitará a sintáxe da regex e os valores padrões entrarão. O mesmo para o comentário, só pode "s", "y", "n" ou "/". Regex: "\\{-?\d?,?[ysn/]?\\}"

">Consegue diminuir os custos?         
{3,y}"
>Observe que usei "y", "yes", ao invés de "s", "sim". Pode ser qualquer um dos dois. Além disso, observe que a sintáxe é flexível, esse \n não afetaria a pergunta. Por fim, "/" é o mesmo que "n", mas é uma forma visual de dizer "não sei".

`;` Por fim, para finalizar a pergunta, o famoso ";".

Exemplo de perguntas:
```
> pergunta válida; -->pergunta válida{2,y};
> pergunta 
  válida{3};
                    ---->   pergunta válida     {};
```
#### -modos como as perguntas podem ser usadas
Tendo as perguntas em mão, o programa lhe entrega um resultado dependendo do modo que você o define, ex: `mode: yorn`. Para definir o modo que o programa executará, basta escrever no topo do seu arquivo. São 3 os possíveis modos: "yorn", "toanswer" e "tofeedback".
#### mode: yorn
yorn é o modo padrão caso nenhum seja definido. O que faz? Ele lê as perguntas e seus parâmetros, pergunta a resposta via terminal ao usuário e gera um feedback. Voltemos ao "projeto x", supusemos que Bob respondesse as perguntas, um possível resultado seria:
![image](https://github.com/user-attachments/assets/dbad07d2-2a7c-445e-b786-75747dc078e4)

#### mode: toanswer
O que aconteceria se pusessemos as mesmas perguntas, mas mudassemos o modo para "toanswer"? Aconteceria que o programa nos daria um arquivo pronto para ser respondido:
```
mode: toanswer
>Consegue entregar uma versão básica de teste ainda nesse mês? {9};
>Consegue diminuir os custos? {5,s};
>Consegue mudar o nome do projeto para o nome do diretor geral?;
```
![image](https://github.com/user-attachments/assets/15c43c20-6449-4bbd-8277-ebcc41d5d726)

É para isso que serve o "toanswer", caso você tenha um grande arquivo de texto e queira separar algumas perguntas enqaunto o lê. Você pode introduzí-las diretamente no arquivo e o "toanswer" pegará apenas o que separou. Ou se você simplesmente não quiser responder as perguntas via terminal, o "toanswer" lhe entrega um formato "tofeedback".
#### mode: tofeedback
"tofeedback" é a mesma coisa que o yorn, mas você introduz as respostas diretamente no arquivo ao invés de dá-las via terminal. A sintáxe nova que você viu é dele, `(a:/ c:/);`, vamos dismiuçá-la:

`()` Os argumentos devem estar entre parênteses e eles devem estar colados com o ";" final da pergunta. Essa parte não é muito flexível... ">pergunta; ()", esse espaço entre a pergunta e a resposta invalidaria a resposta.

`a:` A resposta (pode ser "a:", "answer", ou "r:", "resposta") é um argumento obrigatório e espera "s", "y", "n" ou "/". Se não respondido, a pergunta será ignorada. 
"(a:s)"

`c:` O comentário é um argumento opcional. Observe que se a pergunta tiver "{n}" como parâmetro, mesmo que tenha posto comentário, ele não aparecerá.
"(a:n c:)"

`;` Novamente o ";" para finalizar. Note que a pergunta e a resposta têm ";" individuais.

exemplos de respostas:
```
>...;(r:s);    válido
>...;  (r:s);  inválido(espaço entre a pergunta e resposta)
>...;(c:oi);   inválido(não tem resposta...)
>...;(r:n
c: bla bla);   válido
>...;(r:s)     inválido(sem o ";")
```
>Um adendo importante é que o "yorn" ignora o bloco de resposta `(r:/ c:/);` e o "tofeedback" não pega perguntas não respondidas, então o "toanswer" pode ser usado para ambos os modos.
#### -porcentagem e pontos
Nos exemplos acima você deve ter visto as variáveis `percentage, total_points` e `user_points` nos arquivos gerados para feedback. Essa é a forma como o programa valida sucesso ou falha. No caso, ele soma todos os pontos positivos das perguntas e vê se o tanto de pontos que o usuário fez atende à porcentagem requirida. Isso significa que, colocar perguntas com pontos negativos inverte a lógica do sim/não, fazendo com que o usuário perca pontos ao responder sim, e que é possível manipular a tolerância de erro do programa.
#### feedback: 60
Como visto no arquivo gerado pelo "toanswer", a variável usada para controlar a porcentagem é "feedback:", cujo valor padrão é 60. Da mesma forma como o "mode", basta pô-la no topo do arquivo.
>A verdade é que você pode colocar onde quiser no arquivo, mas é melhor seguir um padrão. Além de que, se puser mais de um, tanto do "mode", quanto do "feedback", o programa pegará apenas a primeira ocorrência.
#### -comandos
`/back` Caso você esteja respondendo uma pergunta no modo "yorn" e dê uma resposta errada, pode usar o comando `/back`, no terminal, para retornar uma pergunta.

`c/on c/off` E, para finalizar, caso você queira configrar várias perguntas para permitir ou não comentário, basta usar os comandos `c/on ou c/off` no arquivo e todos as perguntas, sem parâmetro de comentário definido, logo abaixo do comando obedecerão.
>A hierarquia do comentário é: parâmetro 1°, comando 2°. Isso significa que, se você definir `c/on` no topo do arquivo, o padrão será esse até que você defina outro...

Ex:
```
> pergunta sem comentário;
> pergunta com comentário{s};
c/on
> pergunta com comentário;
> pergunta sem comentário{n};
```
#
---
## Considerações finais
É isso, eu acho. yorn_checklist foi meu primeiro projeto de verdade. Nele usei um monte de coisas que tenho aprendido até agora: `file I/O`, `regex`, `python POO`, `Git/GitHub`... Atualmente tenho 3/4 mêses de programação, mas, apesar de iniciante, sinto que consegui fazer algo desacente. O código teve várias versões que você pode explorar pelos commits ou pela conversa que tive com o gemini, dê uma olhada!

-[Conversa em que o Gemini me auxilia](https://g.co/gemini/share/c3bdb15909d6)

-[Meu Linkedin](https://br.linkedin.com/in/davi-capitano-97a080250)
