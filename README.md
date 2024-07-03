# 🤖 Bot de Autenticação do Discord

Este é um bot de Discord que autentica novos membros com base no endereço de e-mail institucional fornecido. Ele também cria cargos e canais necessários no servidor.

## 💻 Instalação
- Clone este repositório ou copie os arquivos para o seu ambiente local.
- Instale as dependências necessárias:
```
pip install discord.py
```
- Certifique-se de que você tem um arquivo chamado emails.py que contém duas listas: 'alunos' e 'professores', com os e-mails dos alunos e professores respectivamente.
- Crie um bot no [Discord Developer Portal](https://discord.com/developers/docs/intro) e obtenha o token do bot.
- Configure o arquivo para armazenar seu token do bot:
```
DISCORD_TOKEN=seu_token_aqui

```

## ⚙️ Funcionalidades
### Criação de Cargos e Canais:

- O bot criará os cargos Coordenador, Aluno, Professor, Dev, Egresso e Pretendente se eles não existirem.
- Ele também criará a categoria Engenharia de Computação e os canais bem-vindo, regras, avisos-da-coordenacao, oportunidades-de-emprego, oportunidades-internas, duvidas, off-topic e professores se não existirem.

### Autenticação de Novos Membros:

Quando um novo membro entra no servidor, o bot atribui o cargo Pretendente a ele e envia uma mensagem pedindo o e-mail institucional.

O membro tem até 5 tentativas para fornecer um e-mail válido.

Se o e-mail for válido, o bot atribui o cargo apropriado (Aluno ou Professor) e remove o cargo Pretendente.

Se o e-mail não for válido ou o membro exceder o número de tentativas ou o tempo limite, o bot banirá o membro do servidor.
