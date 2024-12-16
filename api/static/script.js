const backendUrl = window.location.origin;  // automaticamente o domínio + a porta

// Função para alternar entre modo claro e escuro
function toggleDarkMode() {
    // Alterna a classe 'dark-mode' no body
    document.body.classList.toggle('dark-mode');

    // Atualiza o emoji do botão
    const button = document.getElementById('theme-toggle');
    if (document.body.classList.contains('dark-mode')) {
        button.innerHTML = "🌞"; // Emoji do sol para modo claro
    } else {
        button.innerHTML = "🌙"; // Emoji da lua para modo escuro
    }
}

// Adicionando o evento para o botão de alternar tema
document.querySelector('#theme-toggle').addEventListener('click', toggleDarkMode);

// Listener para o formulário de upload
document.querySelector('#upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Impede o comportamento padrão do formulário

    // Captura os campos do formulário
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const imageFile = document.getElementById("image").files[0];

    // Verifica se uma imagem foi selecionada
    if (!imageFile) {
        alert("Por favor, selecione uma imagem.");
        return;
    }

    // Cria um FormData para enviar a imagem
    const formData = new FormData();
    formData.append("image", imageFile);

    // Mostra a barra de carregamento
    const loadingBar = document.getElementById("loading");
    loadingBar.style.display = "block";

    try {
        // Faz a requisição para o servidor
        const response = await fetch(`${backendUrl}/classify`, {
            method: 'POST',
            headers: {
                "Authorization": "Basic " + btoa(`${username}:${password}`) // Adiciona o cabeçalho de autenticação
            },
            body: formData
        });

        // Oculta a barra de carregamento
        loadingBar.style.display = "none";

        // Processa a resposta do servidor
        if (response.ok) {
            const data = await response.json();
            document.getElementById('result').innerHTML = `
                <strong>Imagem:</strong> ${data.image_name} <br>
                <strong>Predição:</strong> ${data.prediction} <br>
                <strong>Confiança:</strong> ${data.confidence.toFixed(2)} <br>
            `;
        } else {
            const error = await response.json();
            document.getElementById('result').innerHTML = `
                <p><strong>Erro:</strong> ${error.error}</p>
            `;
        }
    } catch (error) {
        // Trata erros inesperados
        loadingBar.style.display = "none";
        document.getElementById('result').innerHTML = `
            <p><strong>Erro:</strong> Não foi possível processar a requisição.</p>
        `;
        console.error("Erro na requisição:", error);
    }
});


// Alternar visibilidade da senha
document.getElementById('toggle-password').addEventListener('change', function() {
    const passwordField = document.getElementById('password');
    passwordField.type = this.checked ? 'text' : 'password';
});