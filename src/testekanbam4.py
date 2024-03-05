import streamlit as st
import uuid

def kanban_board(tasks_todo, tasks_in_progress, tasks_done):
    st.markdown(
        """
        <style>
            .kanban-container {
                display: flex;
                justify-content: space-between;
                padding: 20px;
            }
            .column {
                flex: 1;
                background-color: #f4f4f4;
                border-radius: 5px;
                padding: 20px;
                margin: 0 10px;
                min-width: 250px;
            }
            .column-header {
                text-align: center;
                margin-bottom: 20px;
            }
            .card {
                background-color: #ffffff;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }
            .todo {
                background-color: #ffd700; /* amarelo */
            }
            .in-progress {
                background-color: #87ceeb; /* azul claro */
            }
            .done {
                background-color: #98fb98; /* verde claro */
            }
        </style>
        """
        ,
        unsafe_allow_html=True,
    )

    #st.subheader("Quadro de Ações")
    st.title("Quadro de Ações")
    # Campo de texto e botão abaixo do título "Quadro de Ações"
    new_task = st.text_input("Nova Tarefa", "", key=str(uuid.uuid4()))
    if st.button("Cadastrar Ação", key=str(uuid.uuid4())):
        if new_task:
            tasks_todo.append(new_task)

    
def main():
    tasks_todo = []
    tasks_in_progress = []
    tasks_done = []

    kanban_board(tasks_todo, tasks_in_progress, tasks_done)

    

    col1, col2, col3 = st.columns(3)

    with col1:
        tasks_todo = st.text_area("A Fazer", height=300).split("\n")

    with col2:
        tasks_in_progress = st.text_area("Em Andamento", height=300).split("\n")

    with col3:
        tasks_done = st.text_area(" Realizado", height=300).split("\n")

    #kanban_board(tasks_todo, tasks_in_progress, tasks_done)



    with col1:
        for task in tasks_todo:
            st.text(task)
        if st.button("Mover para Em Andamento"):
            pass  # Adicione aqui a lógica para mover as tarefas de "A fazer" para "Em andamento"

    with col2:
        
        for task in tasks_in_progress:
            st.text(task)
        if st.button("Mover para Concluído"):
            pass  # Adicione aqui a lógica para mover as tarefas de "Em andamento" para "Concluído"

    with col3:
        for task in tasks_done:
            st.text(task)
        if st.button("Remover"):
            pass  # Adicione aqui a lógica para remover as tarefas concluídas


if __name__ == "__main__":
    main()