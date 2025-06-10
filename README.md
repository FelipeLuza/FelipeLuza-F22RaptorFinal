# Projeto: F-22 Raptor – Zona de Combate

**Última atualização:** Junho de 2025

## 👨‍💻 Desenvolvedor
- **Nome:** Felipe Luza  
- **RA:** 1136806

## 🎮 Descrição do Jogo
Neste jogo, o jogador assume o controle de um caça F-22 em uma zona de combate intensa.  
Mísseis inimigos caem do céu e o objetivo é desviar dos ataques, sobreviver o máximo de tempo possível e acumular pontos.

À medida que a partida avança, a dificuldade aumenta, exigindo reflexos rápidos e precisão.  
A experiência combina ação, tensão e desafio, sendo ideal para testar os limites do jogador.

## 🛠️ Tecnologias Utilizadas
- Python 3.13 (compatível com Python 3.11)
- `Pygame`
- `pyttsx3` (síntese de voz)
- `speech_recognition` (reconhecimento de voz)
- `json` (armazenamento de dados)
- `datetime` (registro de data/hora)
- `cx_Freeze` (empacotamento para executável)
- Git (controle de versão)

## 🚀 Funcionalidades
- Tela de menu com som de comunicação
- Entrada do nome do jogador via teclado
- Comando de voz para iniciar (diga "jogar" após pressionar TAB)
- Voz personalizada com o nome do jogador
- Sistema de pontuação com log em `log.dat`
- Dificuldade progressiva
- Elementos decorativos: sol pulsante e caça inimigo voador
- Efeitos sonoros de míssil, explosão e comunicação
- Tela de Game Over com exibição dos últimos registros
- Função de pausa com tecla `ESPACO`

## 💡 Observações
- O projeto foi desenvolvido e empacotado no **macOS (Apple Silicon)**.
- Para executar em **Windows**:
  - Utilize `python main.py` (com Python 3.11+ e bibliotecas instaladas); ou  
  - Gere um executável `.exe` com `python setup.py build` usando `cx_Freeze`.

