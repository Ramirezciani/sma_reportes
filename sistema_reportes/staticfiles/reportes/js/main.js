class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.cache = new Map();
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const cacheKey = `${url}?${new URLSearchParams(options.params || {}).toString()}`;
        
        // Return cached response if available
        if (options.method === 'GET' && this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers,
                credentials: 'include'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || error.message || 'Request failed');
            }

            const data = await response.json();
            
            // Cache GET responses
            if (options.method === 'GET') {
                this.cache.set(cacheKey, data);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // API endpoints with filtering support
    getOrganismos(params = {}) {
        return this.request('/organismos-sectoriales/', { params });
    }

    getPpdaPlanes(params = {}) {
        return this.request('/planes-ppda/', { params });
    }

    getMedidasAvance(params = {}) {
        return this.request('/medidas-avance/', { params });
    }

    getReportesAnuales(params = {}) {
        return this.request('/reportes-anuales/', { params });
    }

    getResumenAnual() {
        return this.request('/reportes-anuales/resumen_anual/');
    }

    getMedidasPorPPDA(ppdaId) {
        return this.request(`/planes-ppda/${ppdaId}/medidas/`);
    }
}

class DataRenderer {
    static renderTable(data, fields, options = {}) {
        if (!data?.length) return '<div class="no-data">No hay datos disponibles</div>';
        
        const { pagination = false, page = 1, perPage = 10 } = options;
        const startIdx = (page - 1) * perPage;
        const paginatedData = pagination ? 
            data.slice(startIdx, startIdx + perPage) : 
            data;

        return `
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            ${fields.map(f => `<th>${f.label}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${paginatedData.map(item => `
                            <tr>
                                ${fields.map(f => `
                                    <td data-label="${f.label}">
                                        ${f.formatter ? f.formatter(item[f.key]) : (item[f.key] || '-')}
                                    </td>
                                `).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                ${pagination && data.length > perPage ? `
                    <div class="pagination">
                        ${Array.from({ length: Math.ceil(data.length / perPage) }, (_, i) => `
                            <button class="page-btn ${i + 1 === page ? 'active' : ''}" 
                                    onclick="handlePageChange(${i + 1})">
                                ${i + 1}
                            </button>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }

    static renderChart(data, elementId, config) {
        // Implementation would use Chart.js or similar
        return `
            <canvas id="${elementId}" width="400" height="200"></canvas>
            <script>
                new Chart(document.getElementById('${elementId}'), ${JSON.stringify(config)});
            </script>
        `;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const api = new ApiService();
    const loadingHTML = '<div class="loading-spinner"></div>';
    let currentPage = 1;

    // Formularios modales
    const forms = {
        organismo: document.getElementById('organismoForm'),
        ppda: document.getElementById('ppdaForm'),
        medida: document.getElementById('medidaForm')
    };

    // Botones de carga
    const loadButtons = {
        organismo: document.getElementById('fetch-organismos'),
        ppda: document.getElementById('fetch-ppda'),
        medida: document.getElementById('fetch-medidas')
    };

    // Listas de datos
    const dataContainers = {
        organismo: document.getElementById('organismos-list'),
        ppda: document.getElementById('ppda-list'),
        medida: document.getElementById('medidas-list')
    };

    // Global error handler
    window.handleError = (error) => {
        console.error('Global error:', error);
        alert(`Error: ${error.message}`);
    };

    // Improved data loading with filters and pagination
    async function loadData(endpoint, renderFn, targetElement, params = {}) {
        try {
            targetElement.innerHTML = loadingHTML;
            const data = await api[`get${endpoint}`](params);
            targetElement.innerHTML = renderFn(data, {
                pagination: true,
                page: currentPage
            });
        } catch (error) {
            targetElement.innerHTML = `
                <div class="error-message">
                    <p>Error: ${error.message}</p>
                    <button class="retry-btn" onclick="loadData('${endpoint}', ${renderFn}, 
                        document.getElementById('${targetElement.id}'), ${JSON.stringify(params)})">
                        Reintentar
                    </button>
                </div>
            `;
            handleError(error);
        }
    }

    // Handle page changes
    window.handlePageChange = (page) => {
        currentPage = page;
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
            const endpoint = activeTab.dataset.endpoint;
            const targetId = activeTab.dataset.target;
            loadData(endpoint, tablesConfig[endpoint].renderFn, document.getElementById(targetId));
        }
    };

    // Configure data tables with enhanced fields and formatters
    const tablesConfig = {
        'Organismos': {
            fields: [
                { key: 'id', label: 'ID' },
                { key: 'nombre', label: 'Nombre' },
                { key: 'sigla', label: 'Sigla' },
                { 
                    key: 'actividades_count', 
                    label: 'Actividades',
                    formatter: (value) => value || '0'
                }
            ],
            renderFn: (data) => DataRenderer.renderTable(data, tablesConfig.Organismos.fields)
        },
        'PpdaPlanes': {
            fields: [
                { key: 'id', label: 'ID' },
                { key: 'nombre', label: 'Nombre' },
                { key: 'anio', label: 'Año' },
                { 
                    key: 'medidas_count', 
                    label: 'Medidas',
                    formatter: (value) => value || '0'
                }
            ],
            renderFn: (data) => DataRenderer.renderTable(data, tablesConfig.PpdaPlanes.fields)
        },
        'MedidasAvance': {
            fields: [
                { key: 'id', label: 'ID' },
                { key: 'nombre', label: 'Nombre' },
                { 
                    key: 'porcentaje_avance', 
                    label: 'Avance',
                    formatter: (value) => `
                        <div class="progress-bar">
                            <div class="progress" style="width: ${value}%"></div>
                            <span>${value}%</span>
                        </div>
                    `
                },
                { key: 'estado', label: 'Estado' }
            ],
            renderFn: (data) => DataRenderer.renderTable(data, tablesConfig.MedidasAvance.fields)
        }
    };

    // Initialize UI with tabs and filters
    function initUI() {
        // Set up tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const endpoint = tab.dataset.endpoint;
                const targetId = tab.dataset.target;
                loadData(endpoint, tablesConfig[endpoint].renderFn, document.getElementById(targetId));
            });
        });

        // Set up filter forms
        document.querySelectorAll('.filter-form').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const params = Object.fromEntries(formData.entries());
                
                const activeTab = document.querySelector('.tab.active');
                if (activeTab) {
                    const endpoint = activeTab.dataset.endpoint;
                    const targetId = activeTab.dataset.target;
                    loadData(endpoint, tablesConfig[endpoint].renderFn, 
                        document.getElementById(targetId), params);
                }
            });
        });

        // Load initial data
        const initialTab = document.querySelector('.tab.active');
        if (initialTab) {
            const endpoint = initialTab.dataset.endpoint;
            const targetId = initialTab.dataset.target;
            loadData(endpoint, tablesConfig[endpoint].renderFn, document.getElementById(targetId));
        }

        // Load summary chart
        loadSummaryChart();
    }

    // Load summary chart data
    async function loadSummaryChart() {
        try {
            const resumen = await api.getResumenAnual();
            const chartContainer = document.getElementById('resumen-chart');
            if (chartContainer) {
                chartContainer.innerHTML = DataRenderer.renderChart(resumen, 'annual-summary-chart', {
                    type: 'bar',
                    data: {
                        labels: resumen.map(item => item.periodo),
                        datasets: [{
                            label: 'Promedio de Cumplimiento',
                            data: resumen.map(item => item.promedio_cumplimiento),
                            backgroundColor: 'rgba(54, 162, 235, 0.5)'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            }
        } catch (error) {
            handleError(error);
        }
    }

    // Initialize the application
    initUI();
    setupFormHandlers();
});

// Configura los manejadores de eventos para los formularios
function setupFormHandlers() {
    // Manejador para formulario de organismo
    forms.organismo.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleFormSubmit('organismos-sectoriales/', forms.organismo, 'organismo');
    });

    // Manejador para formulario de PPDA
    forms.ppda.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleFormSubmit('planes-ppda/', forms.ppda, 'ppda');
    });

    // Manejador para formulario de medida
    forms.medida.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleFormSubmit('medidas-avance/', forms.medida, 'medida');
    });

    // Configurar botones de carga
    loadButtons.organismo.addEventListener('click', () => loadData('Organismos', tablesConfig.Organismos.renderFn, dataContainers.organismo));
    loadButtons.ppda.addEventListener('click', () => loadData('PpdaPlanes', tablesConfig.PpdaPlanes.renderFn, dataContainers.ppda));
    loadButtons.medida.addEventListener('click', () => loadData('MedidasAvance', tablesConfig.MedidasAvance.renderFn, dataContainers.medida));
}

// Maneja el envío de formularios
async function handleFormSubmit(endpoint, form, type) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Guardando...';

    try {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Convertir fechas a formato ISO
        if (data.fecha_inicio) data.fecha_inicio = new Date(data.fecha_inicio).toISOString();
        if (data.fecha_termino) data.fecha_termino = new Date(data.fecha_termino).toISOString();

        // Enviar datos al servidor
        const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        // Mostrar mensaje de éxito
        alert(`${type.charAt(0).toUpperCase() + type.slice(1)} creado exitosamente`);
        
        // Recargar datos
        loadData(type === 'organismo' ? 'Organismos' : 
                type === 'ppda' ? 'PpdaPlanes' : 'MedidasAvance',
                tablesConfig[type === 'organismo' ? 'Organismos' : 
                           type === 'ppda' ? 'PpdaPlanes' : 'MedidasAvance'].renderFn,
                dataContainers[type]);

        // Cerrar modal y limpiar formulario
        $(`#${type}Modal`).modal('hide');
        form.reset();

    } catch (error) {
        console.error('Error al guardar:', error);
        alert(`Error al guardar: ${error.message}`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}
