// Configurações customizadas para os gráficos do Chart.js
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.color = '#6c757d';
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 0, 0, 0.7)';
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// Função para criar gráfico de pizza para estatísticas
function criarGraficoPizza(ctx, dados) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['0-40%', '40-60%', '60-80%', '80-100%'],
            datasets: [{
                data: dados,
                backgroundColor: [
                    '#dc3545',
                    '#ffc107',
                    '#17a2b8',
                    '#28a745'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Função para criar gráfico de linha com melhorias
function criarGraficoLinha(ctx, labels, dados, cor = 'rgb(75, 192, 192)') {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Desempenho',
                data: dados,
                borderColor: cor,
                backgroundColor: cor.replace('rgb', 'rgba').replace(')', ', 0.1)'),
                tension: 0.4,
                fill: true,
                pointBackgroundColor: cor,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Função para atualizar gráficos em tempo real
function atualizarGraficoPeriodicamente(grafico, urlDados, intervalo = 30000) {
    setInterval(() => {
        fetch(urlDados)
            .then(response => response.json())
            .then(novosDados => {
                grafico.data.labels = novosDados.labels;
                grafico.data.datasets[0].data = novosDados.pontuacoes;
                grafico.update('quiet');
            })
            .catch(erro => console.error('Erro ao atualizar gráfico:', erro));
    }, intervalo);
}