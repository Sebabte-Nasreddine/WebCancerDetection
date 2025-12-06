// ========== DASHBOARD UTILITIES ==========

class Dashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboardData();
        this.setupCharts();
    }

    setupEventListeners() {
        // Ajouter des listeners si nécessaire
        document.addEventListener('DOMContentLoaded', () => {
            this.animateStatCards();
        });
    }

    // Charger les données du dashboard
    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard/stats');
            if (response.ok) {
                const data = await response.json();
                this.updateStatsCards(data);
            }
        } catch (error) {
            console.error('Erreur lors du chargement des données:', error);
        }
    }

    // Mettre à jour les cartes de statistiques
    updateStatsCards(data) {
        const statsContainer = document.querySelector('.dashboard-stats');
        if (!statsContainer) return;

        const cards = statsContainer.querySelectorAll('.stat-card');
        
        if (data.totalPredictions !== undefined) {
            const card = cards[0];
            if (card) {
                card.querySelector('.stat-value').textContent = data.totalPredictions;
            }
        }

        if (data.positiveCases !== undefined) {
            const card = cards[1];
            if (card) {
                card.querySelector('.stat-value').textContent = data.positiveCases;
                card.classList.add('danger');
            }
        }

        if (data.accuracy !== undefined) {
            const card = cards[2];
            if (card) {
                card.querySelector('.stat-value').textContent = (data.accuracy * 100).toFixed(2) + '%';
                card.classList.add('success');
            }
        }
    }

    // Animer les cartes de statistiques
    animateStatCards() {
        const cards = document.querySelectorAll('.stat-card');
        cards.forEach((card, index) => {
            card.style.animation = `slideInUp 0.6s ease-out ${index * 0.1}s both`;
        });
    }

    // Configurer les graphiques
    setupCharts() {
        // À implémenter avec Chart.js ou Plotly
        console.log('Charts setup');
    }

    // Exporter les données
    exportData(format = 'csv') {
        const timestamp = new Date().toISOString().slice(0, 10);
        const filename = `dashboard-export-${timestamp}.${format}`;

        // Récupérer les données
        const table = document.querySelector('.metrics-table');
        if (!table) {
            alert('Aucune donnée à exporter');
            return;
        }

        let content = '';
        
        if (format === 'csv') {
            content = this.tableToCSV(table);
        } else if (format === 'json') {
            content = this.tableToJSON(table);
        }

        this.downloadFile(content, filename, format);
    }

    // Convertir le tableau en CSV
    tableToCSV(table) {
        const rows = [];
        table.querySelectorAll('tr').forEach(row => {
            const cols = [];
            row.querySelectorAll('td, th').forEach(col => {
                cols.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
            });
            rows.push(cols.join(','));
        });
        return rows.join('\n');
    }

    // Convertir le tableau en JSON
    tableToJSON(table) {
        const headers = [];
        const data = [];

        table.querySelectorAll('thead th').forEach(th => {
            headers.push(th.textContent.trim());
        });

        table.querySelectorAll('tbody tr').forEach(tr => {
            const row = {};
            tr.querySelectorAll('td').forEach((td, index) => {
                row[headers[index]] = td.textContent.trim();
            });
            data.push(row);
        });

        return JSON.stringify(data, null, 2);
    }

    // Télécharger un fichier
    downloadFile(content, filename, format) {
        const mimeType = format === 'csv' ? 'text/csv' : 'application/json';
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }

    // Rafraîchir le dashboard
    refresh() {
        console.log('Refreshing dashboard...');
        this.loadDashboardData();
    }

    // Imprimer le dashboard
    printDashboard() {
        window.print();
    }
}

// ========== INITIALISATION ==========
let dashboard;

document.addEventListener('DOMContentLoaded', () => {
    dashboard = new Dashboard();
});

// Ajouter des animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Exposer les fonctions globalement
window.Dashboard = Dashboard;
window.exportData = (format) => dashboard.exportData(format);
window.refreshDashboard = () => dashboard.refresh();
window.printDashboard = () => dashboard.printDashboard();
