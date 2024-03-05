from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Inicializa as listas de tarefas
lista_a_fazer = []
lista_em_andamento = []
lista_concluido = []

@app.route('/', methods=['GET', 'POST'])
def kanban():
    if request.method == 'POST':
        if 'nova_tarefa' in request.form:
            nova_tarefa = request.form['nova_tarefa']
            if nova_tarefa:
                lista_a_fazer.append(nova_tarefa)
        elif 'mover_em_andamento' in request.form:
            selecionada = int(request.form['mover_em_andamento'])
            tarefa = lista_a_fazer.pop(selecionada)
            lista_em_andamento.append(tarefa)
        elif 'mover_concluido' in request.form:
            selecionada = int(request.form['mover_concluido'])
            tarefa = lista_em_andamento.pop(selecionada)
            lista_concluido.append(tarefa)
        elif 'remover_tarefa' in request.form:
            selecionada = int(request.form['remover_tarefa'])
            lista_concluido.pop(selecionada)
        return redirect(url_for('kanban'))
    return render_template('kanban.html', lista_a_fazer=lista_a_fazer, lista_em_andamento=lista_em_andamento, lista_concluido=lista_concluido)

if __name__ == '__main__':
    app.run(debug=True)