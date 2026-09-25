# COMO USAR O INSTACLEANER
### 1. Crie um arquivo na raíz do projeto chamado `instagram` sem nenhuma extensão. Apenas isso.

### 2. Abra o arquivo instagram e cadastre as seguintes variáveis:
```
INSTAGRAM_PERFIL=nome do seu perfil
INSTAGRAM_USERNAME=seu nome de usuário
INSTAGRAM_PASSWORD=sua senha
```
### 3. Usando um terminal, crie um ambiente virtual para o Python na raízo do projeto:
```
py -m venv .venv
```
### 4. Ative o ambiente virtual que você acabou de criar:
```
🪟 Windows: .\.venv\Scripts\activate
🐧 Linux: source ./venv/bin/activate
```
Resultado: `(.venv) seu prommpt Windows/Linux`

### 5. Com o ambiente virtual ativado, importe as bibliotecas:
```
pip install -r requirements.txt
```
### 6. Agora execute a aplicação:
```
py cleanup_instagram.py
```
Caso você use um segundo fator de segurança, não se preocupe pois a aplicação não grava informações sigilosas em cookies. Mantém apenas ativo na seção do terminal. Enquanto a aplicação estiver rodando/funcionando, o 2FA estará registrado. Uma vez que o terminal é fechado, essa informação é excluída e o mesmo código não funcionará mais.

`
Código 2FA do Instagram: * * * * * *
`
