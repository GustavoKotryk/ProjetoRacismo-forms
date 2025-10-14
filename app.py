from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime, timezone, timedelta

fuso_brasil = timezone(timedelta(hours=-3))

app = Flask(__name__)

# Perguntas sobre racismo
PERGUNTAS = [
    {
        'id': 1,
        'pergunta': 'O que é racismo estrutural?',
        'opcoes': [
            'Ações individuais de discriminação racial',
            'Sistema que perpetua desigualdades raciais na sociedade',
            'Preconceito apenas em palavras',
            'Problema que não existe mais no Brasil'
        ],
        'resposta_correta': 1,
        'pontuacao': 10
    },
    {
        'id': 2,
        'pergunta': 'O que caracteriza racismo institucional?',
        'opcoes': [
            'Piadas entre amigos',
            'Discriminação embutida em políticas e instituições',
            'Preferências pessoais por determinada etnia',
            'Livre expressão de opiniões'
        ],
        'resposta_correta': 1,
        'pontuacao': 10
    },
    {
        'id': 3,
        'pergunta': 'Qual é o conceito de colorismo?',
        'opcoes': [
            'Gosto por cores na moda',
            'Discriminação baseada no tom de pele dentro do mesmo grupo racial',
            'Preferência por pessoas de pele clara apenas',
            'Sistema de cores para classificação racial'
        ],
        'resposta_correta': 1,
        'pontuacao': 10
    },
    {
        'id': 4,
        'pergunta': 'O que significa interseccionalidade?',
        'opcoes': [
            'Cruzamento de ruas',
            'Forma de organização social',
            'Análise de como diferentes formas de opressão se conectam',
            'Método matemático para estatísticas'
        ],
        'resposta_correta': 2,
        'pontuacao': 10
    },
    {
        'id': 5,
        'pergunta': 'O que é lugar de fala?',
        'opcoes': [
            'Local onde as pessoas conversam',
            'Importância de ouvir vozes de grupos marginalizados sobre suas próprias experiências',
            'Restrição para quem pode falar sobre certos temas',
            'Técnica de oratória'
        ],
        'resposta_correta': 1,
        'pontuacao': 10
    }
]

# Armazenamento em arquivo JSON (simula "nuvem")
ARQUIVO_DADOS = 'dados_respostas.json'


def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html', perguntas=PERGUNTAS)


@app.route('/submit', methods=['POST'])
def submit_quiz():
    respostas_usuario = request.form.to_dict()
    pontuacao_total = 0
    respostas_corretas = 0
    detalhes_respostas = []

    # Calcular pontuação
    for pergunta in PERGUNTAS:
        resposta_usuario = respostas_usuario.get(f'pergunta_{pergunta["id"]}')
        resposta_correta = pergunta['resposta_correta']

        if resposta_usuario and int(resposta_usuario) == resposta_correta:
            pontuacao_total += pergunta['pontuacao']
            respostas_corretas += 1
            acertou = True
        else:
            acertou = False

        detalhes_respostas.append({
            'pergunta_id': pergunta['id'],
            'pergunta_texto': pergunta['pergunta'],
            'resposta_usuario': int(resposta_usuario) if resposta_usuario else None,
            'resposta_correta': resposta_correta,
            'acertou': acertou
        })

    # Salvar resultados
    dados_existentes = carregar_dados()

    resultado = {
        'id': len(dados_existentes) + 1,
        'timestamp': datetime.now(fuso_brasil).strftime('%d/%m/%Y %H:%M:%S'),  # ← MODIFICADO
        'pontuacao': pontuacao_total,
        'total_perguntas': len(PERGUNTAS),
        'acertos': respostas_corretas,
        'percentual': (pontuacao_total / (len(PERGUNTAS) * 10)) * 100,
        'detalhes_respostas': detalhes_respostas
    }

    dados_existentes.append(resultado)
    salvar_dados(dados_existentes)

    # Gerar feedback
    feedback = gerar_feedback(pontuacao_total, len(PERGUNTAS))

    return render_template('resultado.html',
                           pontuacao=pontuacao_total,
                           total=len(PERGUNTAS) * 10,
                           percentual=resultado['percentual'],
                           feedback=feedback,
                           detalhes=detalhes_respostas)


def gerar_feedback(pontuacao, total_perguntas):
    max_pontos = total_perguntas * 10
    percentual = (pontuacao / max_pontos) * 100

    if percentual >= 80:
        return {
            'titulo': 'Excelente compreensão!',
            'mensagem': 'Você demonstra um bom entendimento sobre racismo e suas nuances estruturais. Continue se informando e combatendo o racismo no dia a dia.',
            'cor': 'success',
            'sugestoes': ['Leia autores negros', 'Participe de debates sobre o tema',
                          'Apoie organizações antirracistas']
        }
    elif percentual >= 60:
        return {
            'titulo': 'Bom conhecimento!',
            'mensagem': 'Você tem uma base sólida, mas pode aprofundar mais no tema do racismo estrutural e institucional.',
            'cor': 'info',
            'sugestoes': ['Estude sobre racismo estrutural', 'Consuma conteúdo de criadores negros',
                          'Reflita sobre privilégios']
        }
    elif percentual >= 40:
        return {
            'titulo': 'Conhecimento básico',
            'mensagem': 'Você tem algumas noções, mas é importante se aprofundar mais no tema para compreender melhor o racismo.',
            'cor': 'warning',
            'sugestoes': ['Leia sobre a história do racismo no Brasil', 'Assista documentários sobre o tema',
                          'Converse com pessoas de diferentes realidades']
        }
    else:
        return {
            'titulo': 'Hora de aprender mais',
            'mensagem': 'Este é um ótimo momento para começar a estudar sobre racismo e suas diferentes manifestações.',
            'cor': 'danger',
            'sugestoes': ['Comece com conteúdos introdutórios', 'Ouça podcasts sobre racismo',
                          'Siga educadores antirracistas']
        }


@app.route('/dados')
def obter_dados():
    dados = carregar_dados()
    dados_grafico = {
        'labels': [f'Tentativa {resultado["id"]}' for resultado in dados],
        'pontuacoes': [resultado['pontuacao'] for resultado in dados],
        'acertos': [resultado['acertos'] for resultado in dados],
        'percentuais': [resultado['percentual'] for resultado in dados]
    }
    return jsonify(dados_grafico)


@app.route('/admin')
def admin():
    dados = carregar_dados()
    return render_template('admin.html', resultados=dados)


@app.route('/limpar_dados', methods=['POST'])
def limpar_dados():
    senha = request.form.get('senha')

    if senha != "senhasuperboa":
        return "Senha incorreta!", 403

    salvar_dados([])
    return redirect('/admin')

@app.route('/health')
def health_check():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)