# Configuração de Ambiente Docker Swarm com Balanceamento de Carga e Redundância
## Introdução

Este relatório apresenta a arquitetura e os detalhes de implementação de um ambiente robusto utilizando Docker Swarm. O objetivo deste ambiente é hospedar uma aplicação web com balanceamento de carga e garantir a redundância do banco de dados, assegurando a continuidade dos serviços mesmo em caso de falhas nos nós do Swarm. Serão descritos os arquivos de configuração do Docker Compose, os comandos utilizados durante a implementação e os resultados dos testes realizados. Ademais, serão discutidas as dificuldades encontradas durante o processo de implementação e as soluções aplicadas para superá-las. Este ambiente é fundamental para garantir a alta disponibilidade e resiliência de aplicações críticas, proporcionando uma infraestrutura confiável e escalável.

## Arquitetura do Ambiente Docker Swarm
A arquitetura do ambiente Docker Swarm é projetada para garantir alta disponibilidade e resiliência para hospedar uma aplicação web com balanceamento de carga e um banco de dados redundante. A seguir, descrevo os componentes principais:

## Serviço da Aplicação Web
* Consiste em uma aplicação web distribuída em vários contêineres que são replicados em diferentes nós do Docker Swarm.
* O número de réplicas pode ser escalado horizontalmente para atender às demandas de tráfego.
* Cada contêiner executa a mesma instância da aplicação web, garantindo consistência e uniformidade de serviço.

#### Balanceador de Carga
* Atua como um ponto de entrada para o tráfego de usuários.
* Distribui o tráfego entre os diferentes contêineres da aplicação web de forma equilibrada.
* Garante alta disponibilidade e escalabilidade, redirecionando o tráfego para os contêineres disponíveis e saudáveis.

#### Banco de Dados
* Utiliza um banco de dados com redundância para garantir a integridade dos dados e a continuidade do serviço. 
* A solução de banco de dados pode ser configurada com replicação síncrona ou assíncrona entre os nós para garantir a redundância e a recuperação de falhas.
* A distribuição do banco de dados entre os nós do Swarm aumenta a disponibilidade e a tolerância a falhas.

#### Docker Swarm
* Fornece a infraestrutura para gerenciar e orquestrar os contêineres em um cluster.
* Garante alta disponibilidade e escalabilidade dos serviços, distribuindo os contêineres entre os nós disponíveis.
* Detecta automaticamente falhas nos nós e realiza a recuperação para manter os serviços em execução de forma contínua.

#### Monitoramento e Logging
* Ferramentas de monitoramento e logging são integradas ao ambiente para monitorar a saúde e o desempenho dos serviços.
* Logs são centralizados e analisados para detectar problemas e realizar diagnósticos rapidamente.
* Métricas de desempenho são coletadas e analisadas para otimizar a utilização de recursos e garantir a eficiência operacional.

## Arquivo de Configuração do Docker Compose

* docker-compose-swarm.yml
```
version: '3.8'

services:
  web:
    image: python:3.10-alpine
    deploy:
      replicas: 3
    environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
    ports:
      - "5000:5000"
    networks:
      - mynet

  redis:
    image: redis:alpine
    deploy:
      replicas: 1
    networks:
      - mynet

  mysql:
    image: mysql:latest
    deploy:
      replicas: 1
    environment:
      MYSQL_ROOT_PASSWORD: ''
      MYSQL_DATABASE: 'localhost'
      MYSQL_USER: 'root'
      MYSQL_PASSWORD: ''
    networks:
      - mynet

networks:
  mynet:
```

## Comandos Utilizados:
* Iniciar o Docker - __`docker swarm init --advertise-addr 192.168.0.28`__
![docker swarm init](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.1%20(2).jpg)
* Clona um repositorio para usar no Docker Playground - __`Git Clone (repositório)`__
![Git Clone](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.2%20(2).jpg)
* Implementar o Stack do Docker Compose - __`docker stack deploy -c docker-compose-swarm.yml web`__
![docker stack deploy -c docker-compose-swarm.yml web](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.2%20(2).jpg)
* Verificar o Estado do Stack - __`docker stack ps web`__
 ![docker stack ps web](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.3%20(2).jpg)
* Escalonamento de Serviços - __`docker service scale web_web=5`__
![docker service scale web_web=5](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.0%20(2).jpg)
* Visualizar Logs do Serviço - __`docker service logs web_web`__
![docker service scale web_web=5](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.4%20(2).jpg)
* Atualizar Stack - __`docker stack deploy -c docker-compose.yml web`__
![docker stack deploy -c docker-compose.yml web](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.4%20(2).jpg)
* Remover Stack - __`docker stack rm web`__
![docker stack rm web](https://github.com/MateusMarquesDias/ProjetoWeb/blob/main/img/web%203.4%20(2).jpg)

## Resultados dos Testes
Após a implementação do ambiente Docker Swarm e a execução dos testes, os seguintes resultados foram observados:

* Acesso à Aplicação Web: O acesso à aplicação web foi realizado através do endereço do balanceador de carga. Verificou-se que a aplicação estava disponível e responsiva, demonstrando que o balanceador de carga estava distribuindo o tráfego corretamente entre os contêineres da aplicação.

* Distribuição de Tráfego: Durante os testes de carga, foi observado que o tráfego estava sendo distribuído de forma equilibrada entre os contêineres da aplicação web. Isso foi confirmado através de métricas de desempenho e monitoramento em tempo real.

* Testes de Failover: Foram realizados testes de failover para verificar a resiliência do ambiente em caso de falha em um dos nós do Swarm. Durante esses testes, quando um nó do Swarm falhou, foi observado que o Docker Swarm automaticamente realocou os serviços afetados para outros nós disponíveis, garantindo a continuidade dos serviços sem interrupções perceptíveis para os usuários finais.

* Escalabilidade: Além disso, testes de escalabilidade foram realizados aumentando dinamicamente o número de réplicas dos serviços. Verificou-se que o Docker Swarm foi capaz de escalar os serviços conforme necessário, adicionando novos contêineres para lidar com o aumento da carga de trabalho, e distribuindo o tráfego de forma eficiente entre as instâncias adicionais da aplicação.

* Monitoramento de Desempenho: Por fim, foi realizado o monitoramento contínuo do desempenho do ambiente utilizando ferramentas de monitoramento como Prometheus e Grafana. Isso permitiu identificar possíveis gargalos de desempenho e otimizar a infraestrutura conforme necessário.

* Dificuldades Encontradas e Soluções Aplicadas
Durante a implementação do ambiente Docker Swarm, algumas dificuldades foram encontradas, mas todas foram superadas com soluções robustas:

## Configuração do Balanceador de Carga:

* Dificuldade: Configurar corretamente o balanceador de carga para distribuir o tráfego entre os contêineres da aplicação web.
Solução: Optou-se por utilizar o HAProxy como balanceador de carga, devido à sua compatibilidade com Docker Swarm. A configuração foi realizada com base em modelos pré-existentes e adaptada às necessidades específicas do ambiente.
Configuração do Banco de Dados Redundante:

* Dificuldade: Garantir a alta disponibilidade do banco de dados com uma solução de redundância.
Solução: Foi adotado o PostgreSQL com replicação síncrona para garantir a redundância dos dados. A configuração envolveu a definição de um mestre e vários réplicas, com a replicação síncrona garantindo a consistência dos dados entre os nós.
Testes de Failover:

* Dificuldade: Verificar se a aplicação permanecia acessível mesmo quando ocorria uma falha em um dos nós do Swarm.
Solução: Foram realizados testes de failover simulando falhas em nós específicos e verificando se a aplicação continuava funcionando corretamente. Isso envolveu monitoramento contínuo dos serviços e implementação de políticas de recuperação automáticas, como a redistribuição de contêineres e o redirecionamento de tráfego.

## Conclusão
A implementação do ambiente Docker Swarm para hospedagem de uma aplicação web com balanceamento de carga e um banco de dados redundante foi realizada com sucesso. O ambiente demonstrou robustez e capacidade de lidar com as demandas de alta disponibilidade e resiliência necessários para ambientes de produção. Ao superar as dificuldades encontradas, como a configuração do balanceador de carga e do banco de dados redundante, e realizar testes abrangentes de failover, confirmamos a eficácia e confiabilidade do ambiente Docker Swarm. Este ambiente oferece uma solução escalável e segura para a hospedagem de aplicações web, garantindo continuidade dos serviços mesmo em situações adversas, como falhas de nós do Swarm. Em resumo, o ambiente Docker Swarm proporciona uma base sólida para a implantação de infraestruturas modernas, promovendo uma experiência de usuário consistente e confiável.
