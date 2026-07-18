# Como colocar o monitor pra rodar sozinho, todo dia, de graça (via GitHub)

Este guia não usa Terminal nem linha de comando — só o site do GitHub, clicando e
arrastando arquivos, como se fosse o Google Drive.

**Importante:** isso é uma tentativa gratuita, mas pode não funcionar — o
Estante Virtual às vezes bloqueia acessos automáticos vindos de "nuvem" (é
diferente do seu Mac, que usa a internet de casa). Vamos tentar e ver o
resultado real. Se não der certo, seguimos com o plano do Mac, que sabemos
que funciona.

---

## Parte 1 — Criar sua conta gratuita no GitHub

1. Abra **github.com** no navegador (pode ser no celular ou computador).
2. Clique em **Sign up** (Criar conta).
3. Preencha e-mail, senha e um nome de usuário. Confirme o e-mail que chegar
   na sua caixa de entrada.
4. Pronto, você tem uma conta gratuita.

---

## Parte 2 — Criar o "repositório" (a pasta do seu projeto)

Um "repositório" é só uma pasta de projeto no GitHub.

1. Já logado, clique no **+** no canto superior direito → **New repository**.
2. Em "Repository name", escreva por exemplo `estante-monitor`.
3. Marque a opção **Private** (assim só você vê o conteúdo).
4. Clique em **Create repository**.

---

## Parte 3 — Subir os arquivos que te mandei

1. Baixe o arquivo `estante-monitor.zip` que te enviei (baixe direto no
   computador, ou no celular e depois transfira — mas o upload em si você
   pode fazer até pelo navegador do celular).
2. Descompacte o `.zip` no seu computador (dois cliques nele costuma
   descompactar sozinho; no Mac, é automático).
3. Volte para a página do seu repositório no GitHub (o que você criou na
   Parte 2).
4. Clique em **Add file** → **Upload files**.
5. Abra a pasta descompactada `estante-monitor` no seu computador e arraste
   **todo o conteúdo de dentro dela** (não a pasta em si, o que está dentro:
   os arquivos `monitor.py`, `config.py`, `autores.py`, `requirements.txt`,
   `README.md`, e a pastinha `.github`) para dentro da janela do navegador.
6. Role para baixo e clique em **Commit changes** (é o botão de "salvar").

Se a pasta `.github` não aparecer pra arrastar (alguns sistemas escondem
pastas que começam com ponto), me avise que te mostro um jeito alternativo
de criar esse arquivo específico direto pelo site do GitHub.

---

## Parte 4 — Telegram (PULE por enquanto)

Para este primeiro teste, o Telegram está desligado — o script só gera a
planilha. Não precisa criar bot nem configurar nada aqui. Quando o teste
funcionar e você quiser ativar os avisos, me avisa que eu te guio nessa parte.

Vá direto para a Parte 5.

---

## Parte 5 — Rodar pela primeira vez (manualmente, para testar)

1. No seu repositório, clique na aba **Actions** (no topo da página).
2. Você deve ver um item chamado **Monitor Estante Virtual** na lista à
   esquerda. Clique nele.
3. Clique no botão **Run workflow** (um menu suspenso vai aparecer) →
   confirme clicando em **Run workflow** de novo.
4. Aguarde. Vai aparecer uma linha nova com uma bolinha amarela (rodando).
   Clique nela pra acompanhar o progresso em tempo real.
5. Quando terminar, a bolinha fica **verde** (deu certo) ou **vermelha** (deu
   erro). Se dor vermelha, me manda um print da tela que eu ajudo a
   entender o que houve.

---

## Parte 6 — Ver o resultado

- Se deu certo, o próprio repositório vai ter um arquivo
  `achados_estante.xlsx` atualizado — clique nele no GitHub e depois em
  **Download** pra abrir no seu computador ou celular.
- Se você configurou o Telegram, deve chegar uma mensagem lá com os achados.

A partir daqui, ele roda **sozinho, todo santo dia, sem você precisar fazer
nada** (o robô do GitHub aciona automaticamente). Você só confere o Telegram
ou baixa a planilha de vez em quando.

---

## Se dor errado (bolinha vermelha)

O motivo mais provável é o bloqueio do site contra acessos automáticos vindos
de "nuvem" (isso é justamente o que estamos testando). Clique na execução
com bolinha vermelha, depois em "Rodar a checagem no Estante Virtual" pra ver
a mensagem de erro, e me manda um print — eu leio e te digo se é isso mesmo
ou se é algo simples de ajustar.

Se for mesmo o bloqueio, seguimos com o plano do Mac, que tem muito mais
chance de funcionar (por usar a internet da sua casa).
