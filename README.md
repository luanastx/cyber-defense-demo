```markdown
# Sistema de Defesa Cibernética — Exemplo Básico (educacional)

- O projeto é um protótipo didático em Python que captura/gera fluxos de rede, transforma os dados,
aplica regras rápidas, treina um classificador (CNN), treina um agente por reforço para decidir bloquear/permitir e gera explicações (XAI).

Tecnologias usadas
- Python 3.8+ — linguagem principal.
- scapy — captura/ leitura de pacotes pcap (extração de fluxos).
- pandas, numpy — manipulação e processamento de dados.
- scikit-learn — transformação e normalização (StandardScaler).
- PyTorch — definição e treino do modelo CNN.
- SHAP — gerar explicações (XAI) das decisões do classificador.
- stable-baselines3 + gym — ambiente e algoritmo de Reinforcement Learning (PPO).
- matplotlib, tqdm — visualização e barras de progresso.
- Git / GitHub CLI (opcional) — versionamento e publicação do repositório.

Arquivos
 
- README.md
  - Explica o projeto, mostra como rodar os passos principais.
- requirements.txt
  - Lista as bibliotecas Python necessárias para rodar o projeto.
- .gitignore
  - Define arquivos/pastas que não devem ser versionados (dados, modelos, venv).
- LICENSE
  - Contém a licença MIT (permissão de uso do projeto).

- src/generate_synthetic.py
  - Gera um CSV com "fluxos" de rede sintéticos (rotulados benigno/malicioso) para testar sem capturar tráfego real.

- src/capture.py
  - Lê um arquivo pcap ou faz sniff na interface e agrega pacotes em fluxos, gerando um CSV com estatísticas por fluxo (pacotes, bytes, duração).

- src/preprocess.py
  - Lê o CSV de fluxos, anonimiza IPs (hash), normaliza as features e salva arrays prontos para treino/inferência (.npz).

- src/heuristics.py
  - Contém regras simples e rápidas (heurísticas) como “muitas tentativas do mesmo IP” ou “muitos pacotes para porta 22” que geram alertas imediatos.

- src/cnn_model.py
  - Define um modelo 1D-CNN simples (em PyTorch) que recebe o vetor de features e produz probabilidade de ser malicioso.

- src/train_cnn.py
  - Script para treinar o modelo CNN com os dados pré-processados e salvar o arquivo de modelo.

- src/rl_env.py
  - Implementa um ambiente Gym simplificado onde cada passo é um fluxo e ação = bloquear ou permitir; define recompensas para treinar o agente.

- src/train_rl.py
  - Treina um agente RL (PPO do stable-baselines3) no ambiente criado para aprender quando bloquear/permitir.

- src/xai_explain.py
  - Usa SHAP para explicar por que o classificador tomou determinada decisão (mostra quais features influenciaram a predição).

Resumo geral

1. Coletamos ou simulamos fluxos de rede e transformamos esses dados em números que a IA entende.  
2. Primeiro aplicamos regras rápidas (heurísticas) e depois um classificador (CNN) para detectar anomalias; um agente de RL aprende a ação (bloquear/permitir) com base em recompensas.  
3. Usamos SHAP para explicar o porquê de cada decisão, e hash/anonymização para proteger a privacidade.

Projeto demonstra um pipeline simplificado para um sistema de defesa cibernética:

- Coleta de dados (pcap ou simulado)
- Pré-processamento
- Regras heurísticas (detecção rápida)
- Classificação com uma pequena CNN (1D) para detectar anomalias
- Aprendizado por Reforço para decidir ações (bloquear / permitir)
- Explicabilidade com SHAP
- Notas de privacidade e ética

Requisitos
- Python 3.8+
- Recomenda instalar em um virtualenv
- Instale dependências:
  pip install -r requirements.txt

Principais scripts
- src/generate_synthetic.py : gera um CSV com fluxos (labels benign/malicious) para teste.
- src/capture.py : captura pacotes (ou lê pcap) e extrai features por fluxo.
- src/preprocess.py : normaliza e transforma CSV em arrays para treino/inferência.
- src/heuristics.py : funções de detecção heurística rápidas.
- src/cnn_model.py, src/train_cnn.py : modelo CNN simples e script de treino.
- src/rl_env.py, src/train_rl.py : ambiente Gym simplificado e treino de agente RL.
- src/xai_explain.py : gera explicações (SHAP) para decisões do classificador.

Privacidade e ética
- Coletar apenas metadados necessários (sem payloads).
- Anonimizar/hashear endereços IP antes de armazenar.
- Logs de decisões e justificativas (XAI) para auditoria.
- Mecanismos de revisão humana antes de ações automatizadas destrutivas.

```
