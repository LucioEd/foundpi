// Função para fazer a chamada da API
async function aprovarCadastro(id) {
    try {
        const url = `/aluno/aprovar/${id}`;        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });        
        const data = await response.json();
        if (data.ok) {
            ocultarTooltipErro(id);
            removerLinhaComAnimacao(id);            
        } else {
            mostrarTooltipErro(id);
        }
    } catch (error) {
        console.error('Erro ao chamar a API:', error);        
    }
}

function removerLinhaComAnimacao(id) {
    const linha = document.querySelector(`tr[data-id="${id}"]`);
    if (linha) {
        const rect = linha.getBoundingClientRect();
        linha.style.height = `${rect.height}px`;
        void linha.offsetHeight;
        linha.classList.add('fade-out');        
        linha.addEventListener('animationend', () => {
            linha.remove();
            recarregarPagina();
        });
    }
}

function ocultarTooltipErro(id) {
    const botao = document.querySelector(`button.btn-success[data-id="${id}"]`);
    if (botao) {
        var tooltip = bootstrap.Tooltip.getInstance(botao);
        tooltip.hide();
    }
}

function mostrarTooltipErro(id) {
    const botao = document.querySelector(`button.btn-success[data-id="${id}"]`);
    if (botao) {
        var tooltip = bootstrap.Tooltip.getInstance(botao);
        tooltip._config.title = "Ocorreu um problema ao tentar aprovar o cadastro.";
        tooltip.update();
        tooltip.show();
        setTimeout(() => {
            tooltip.hide();
        }, 3000);
    }
}

function recarregarPagina() {
    //const trs = document.querySelectorAll('tbody>tr');        
    //if (trs.length === 0) {
    window.location.href = '/aluno/aprovar';
    //}
}

// Adicionar um evento de clique a todos os elementos <a> com classe "btn-success"
document.addEventListener('DOMContentLoaded', (event) => {    
    const botoes = document.querySelectorAll('button.btn-success');
    botoes.forEach((botao) => {
        botao.addEventListener('click', (event) => {
            event.preventDefault();
            const id = botao.getAttribute('data-id');            
            aprovarCadastro(id);
        });
    });
});