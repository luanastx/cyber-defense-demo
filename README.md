```markdown
# Sistema de Defesa Cibernética — Exemplo Básico (educacional)

Este projeto é um protótipo educativo que demonstra um pipeline simplificado para um sistema de defesa cibernética:
- Coleta de dados (pcap ou simulado)
- Pré-processamento
- Regras heurísticas (detecção rápida)
- Classificação com uma pequena CNN (1D) para detectar anomalias
- Aprendizado por Reforço para decidir ações (bloquear / permitir)
- Explicabilidade com SHAP
- Notas de privacidade e ética

Importante:
- Este projeto é didático. Não use em produção sem auditoria, testes e controles de segurança.
- Capturar tráfego em interfaces reais pode requerer privilégios de administrador e envolve dados sensíveis — prefira usar o gerador sintético `generate_synthetic.py` para testes.

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

Exemplo de uso rápido (com dados sintéticos)
1) Gerar dados:
   python src/generate_synthetic.py --output data/flows.csv --n 2000

2) Pré-processar:
   python src/preprocess.py --input data/flows.csv --output data/preprocessed.npz

3) Treinar CNN:
   python src/train_cnn.py --input data/preprocessed.npz --model output/cnn.pth

4) Rodar heurísticas (exemplo):
   python -c "from src.heuristics import detect_heuristics; print('OK')"

5) Treinar RL (usa o dataset rotulado):
   python src/train_rl.py --input data/preprocessed.npz --model output/rl.zip

6) Explicar predição:
   python src/xai_explain.py --model output/cnn.pth --input data/preprocessed.npz

Privacidade e ética (resumo)
- Coletar apenas metadados necessários (sem payloads).
- Anonimizar/hashear endereços IP antes de armazenar.
- Logs de decisões e justificativas (XAI) para auditoria.
- Mecanismos de revisão humana antes de ações automatizadas destrutivas.

Licença: MIT (exemplo). Use com responsabilidade.
```