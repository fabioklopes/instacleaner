# COMO USAR O INSTACLEANER
### 1. Crie um arquivo na raíz do projeto chamado _instagram_ sem nenhuma extensão. Apenas isso.

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
### 5. Com o ambiente virtual ativado, importe as bibliotecas:
```
pip install -r requirements.txt
```
### 6. Agora execute a aplicação:
```
py cleanup_instagram.py
```
