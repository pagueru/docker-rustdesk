# docker-rustdesk

O **[RustDesk](https://github.com/rustdesk/rustdesk)** é uma alternativa open-source ao **AnyDesk**, oferecendo acesso remoto e controle de dispositivos de forma segura e direta, sem depender de serviços de terceiros. Ele proporciona uma experiência semelhante a outras ferramentas comerciais, com a vantagem de ser flexível e baseado em código aberto.

Este repositório oferece a configuração necessária para executar um servidor, utilizando `Docker Compose` para gerenciar os serviços necessários. Além disso, inclui scripts `.bat` gerados em Python, que simplificam a configuração de regras de firewall.

> [!IMPORTANT]  
> A complexidade criada nos scripts não é essencial para a execução do servidor. Para subir um **self-host RustDesk**, basta ter o cliente, executar o `docker-compose` e ter o **Docker Desktop** instalado e em funcionamento.

Os scripts `.bat` mencionados são criados utilizando bibliotecas como `json`, `subprocess`, `pathlib`, `typing`, `logging` e `platform`. O código foi desenvolvido seguindo o máximo possível das boas práticas do **Pylint**, visando garantir a legibilidade e a qualidade do código.

## Documentação Original

- [RustDesk Server Github](https://github.com/rustdesk/rustdesk-server)
- [RustDesk Docker](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/)
- [RustDesk Self-Host](https://rustdesk.com/docs/en/self-host/)
- [Client Configuration](https://rustdesk.com/docs/en/self-host/client-configuration/)

## Requisitos Básicos

O Git é opcional, pois o arquivo `docker-compose.yml` pode ser baixado manualmente, sem a necessidade de clonar o repositório inteiro.

- [Git](https://git-scm.com/downloads)
- [Docker Compose](https://docs.docker.com/desktop/setup/install/windows-install/)
- [RustDesk Client](https://docs.microsoft.com/en-us/windows/wsl/)

Também é possível realizar a instalação utilizando o `winget`:

- `winget install -e --id Git.Git`
- `winget install -e --id Docker.DockerDesktop`
- `winget install -e --id RustDesk.RustDesk`

## Como Utilizar

1. Clone este repositório ou baixe o `docker-compose`:

2. Configure as regras de firewall no Windows usando o comando abaixo ou por meio da interface do **Windows Defender Firewall com Segurança Avançada**:

   ```bash
   netsh advfirewall firewall add rule name="RustDesk Self-Host TCP (21115-21119)" action=allow protocol=tcp localport=21115-21119

   netsh advfirewall firewall add rule name="RustDesk Self-Host UDP (21116)" action=allow protocol=udp localport=21116
   ```

   Utilizando a interface do Windows:

   - Selecione **Regras de Entrada > Nova Regra**.
   - Escolha o tipo de regra como **Porta**.
   - Identifique se é **TCP** ou **UDP** e preencha as portas locais que deseja abrir.
   - Escolha **Permitir Conexão**, mantenha os Perfis marcados (Domínio, Particular e Público), e dê um nome para identificar a regra.

   O Windows permite duplicidade ao criar regras de Firewall com o mesmo nome e portas. Isso não impede o funcionamento, mas é ideal evitar. Caso ocorra, limpe as regras de firewall e execute novamente o processo de criação.

3. Inicie os containers através do terminal com `docker-compose up -d` ou utilizando a interface do **Docker Desktop**.

   Ao executar o `docker-compose`, a pasta `./data/` será gerada localmente no projeto. Essa pasta conterá arquivos como a chave privada (`id_ed25519`) e a chave pública (`id_ed25519.pub`). **Esses arquivos não devem ser alterados ou removidos.**

4. Use o comando `ipconfig` para localizar o endereço IPv4 do seu IP local e configurá-lo no RustDesk Client.

5. Preencha o endereço IPv4 no RustDesk Client em `Configurações > Rede > Servidor ID/Relay`, nos campos `Servidor de ID` e `Servidor de Relay`. O campo `Key` deverá ser preenchido com a chave pública gerada (`./data/id_ed25519.pub`). Isso deve ser configurado nas máquinas que deseja estabelecer a conexão.

Caso tudo esteja configurado corretamente, no RustDesk Client em ambas as máquinas, aparecerá a mensagem `🟢 Pronto` na parte inferior. Caso haja algum problema, pode surgir a mensagem de `🟠 Conectando à rede do RustDesk...`. Se o serviço não estiver em execução, será exibido `🟠 Serviço não está em execução`, com o botão clicável de `Iniciar Serviço`.

## Requisitos Opicionais

Para replicar a geração dos arquivos `.bat`, é necessário instalar o `Python` e suas dependências. Para mais detalhes, consulte o repositóro **[py-default-repo](https://github.com/pagueru/py-default-repo)**.

Ao executar o `main.py`, os scripts gerados estarão na pasta `scripts/output`. Para a criação e remoção das regras, é necessário abrir um terminal como administrador:

- `add_firewall_rules.bat`
- `delete_firewall_rules.bat`
- `verify_firewall_rules.bat`

Use clicando diretamente no arquivo `.bat` ou via terminal no Windows.

## Contato

GitHub: [pagueru](https://github.com/pagueru/)

LinkedIn: [Raphael Henrique Vieira Coelho](https://www.linkedin.com/in/raphaelhvcoelho/)

E-mail: [raphael.phael@gmail.com](mailto:raphael.phael@gmail.com)
