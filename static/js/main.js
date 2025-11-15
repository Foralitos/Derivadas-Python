const examples = window.examplesData || [];

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const tabContents = document.querySelectorAll('.tab-content');

    function switchTab(tabId) {
        tabContents.forEach(content => content.classList.remove('active'));
        tabButtons.forEach(button => button.classList.remove('active'));
        sidebarLinks.forEach(link => link.classList.remove('active'));

        const selectedContent = document.getElementById(tabId);
        if (selectedContent) selectedContent.classList.add('active');

        const selectedButton = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
        if (selectedButton) selectedButton.classList.add('active');

        const selectedLink = document.querySelector(`.sidebar-link[data-tab="${tabId}"]`);
        if (selectedLink) selectedLink.classList.add('active');

        document.querySelector('.content-area').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.getAttribute('data-tab')));
    });

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchTab(link.getAttribute('data-tab'));
        });
    });
}

function createContourPlots(example, containerId) {
    const data = example.plot_data;
    const traces = [
        {
            z: data.Z,
            x: data.x_vector,
            y: data.y_vector,
            type: 'contour',
            colorscale: 'Viridis',
            name: 'f(x,y)',
            xaxis: 'x1',
            yaxis: 'y1',
            colorbar: { x: 0.28 }
        },
        {
            z: data.df_dx,
            x: data.x_vector,
            y: data.y_vector,
            type: 'contour',
            colorscale: 'RdBu',
            name: '∂f/∂x',
            xaxis: 'x2',
            yaxis: 'y2',
            colorbar: { x: 0.63 }
        },
        {
            z: data.df_dy,
            x: data.x_vector,
            y: data.y_vector,
            type: 'contour',
            colorscale: 'RdBu',
            name: '∂f/∂y',
            xaxis: 'x3',
            yaxis: 'y3',
            colorbar: { x: 0.98 }
        }
    ];

    const layout = {
        title: `f(x,y) = ${example.function}`,
        grid: { rows: 1, columns: 3, pattern: 'independent' },
        xaxis: { title: 'x', domain: [0, 0.28], anchor: 'y1' },
        yaxis: { title: 'y', domain: [0, 1], anchor: 'x1' },
        xaxis2: { title: 'x', domain: [0.35, 0.63], anchor: 'y2' },
        yaxis2: { title: 'y', domain: [0, 1], anchor: 'x2' },
        xaxis3: { title: 'x', domain: [0.70, 0.98], anchor: 'y3' },
        yaxis3: { title: 'y', domain: [0, 1], anchor: 'x3' },
        annotations: [
            { x: 0.14, y: 1.05, xref: 'paper', yref: 'paper', text: 'f(x,y)', showarrow: false, font: { size: 14, weight: 'bold' } },
            { x: 0.49, y: 1.05, xref: 'paper', yref: 'paper', text: '∂f/∂x', showarrow: false, font: { size: 14, weight: 'bold' } },
            { x: 0.84, y: 1.05, xref: 'paper', yref: 'paper', text: '∂f/∂y', showarrow: false, font: { size: 14, weight: 'bold' } }
        ],
        height: 400
    };

    Plotly.newPlot(containerId, traces, layout, { responsive: true });
}

function createSurfacePlots(example, containerId) {
    const data = example.plot_data;

    const traces = [
        {
            z: data.Z,
            x: data.x_vector,
            y: data.y_vector,
            type: 'surface',
            colorscale: 'Viridis',
            name: 'f(x,y)',
            scene: 'scene1'
        },
        {
            z: data.df_dx,
            x: data.x_vector,
            y: data.y_vector,
            type: 'surface',
            colorscale: 'RdBu',
            name: '∂f/∂x',
            scene: 'scene2'
        },
        {
            z: data.df_dy,
            x: data.x_vector,
            y: data.y_vector,
            type: 'surface',
            colorscale: 'RdBu',
            name: '∂f/∂y',
            scene: 'scene3'
        }
    ];

    const layout = {
        title: `Superficies 3D: f(x,y) = ${example.function}`,
        grid: { rows: 1, columns: 3, pattern: 'independent' },
        scene1: { domain: { x: [0, 0.28], y: [0, 1] }, xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: 'f' } },
        scene2: { domain: { x: [0.36, 0.64], y: [0, 1] }, xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: '∂f/∂x' } },
        scene3: { domain: { x: [0.72, 1], y: [0, 1] }, xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: '∂f/∂y' } },
        height: 500
    };

    Plotly.newPlot(containerId, traces, layout, { responsive: true });
}

function createVectorPlot(example, containerId) {
    const data = example.plot_data;
    const step = Math.max(1, Math.floor(data.x_vector.length / 20));
    const x_sub = [], y_sub = [], u_sub = [], v_sub = [];

    for (let i = 0; i < data.X.length; i += step) {
        for (let j = 0; j < data.X[0].length; j += step) {
            x_sub.push(data.X[i][j]);
            y_sub.push(data.Y[i][j]);
            u_sub.push(data.df_dx[i][j]);
            v_sub.push(data.df_dy[i][j]);
        }
    }

    const traces = [
        {
            x: data.x_vector,
            y: data.y_vector,
            z: data.Z,
            type: 'contour',
            colorscale: 'Viridis',
            opacity: 0.4,
            showscale: false,
            contours: { coloring: 'heatmap' }
        },
        {
            x: x_sub,
            y: y_sub,
            mode: 'markers',
            marker: {
                size: 5,
                color: u_sub.map((u, i) => Math.sqrt(u * u + v_sub[i] * v_sub[i])),
                colorscale: 'Plasma',
                showscale: true,
                colorbar: { title: '|∇f|' }
            },
            type: 'scatter',
            name: 'Puntos'
        }
    ];

    const annotations = [];
    for (let i = 0; i < Math.min(x_sub.length, 100); i++) {
        const scale = 0.3;
        annotations.push({
            x: x_sub[i] + u_sub[i] * scale,
            y: y_sub[i] + v_sub[i] * scale,
            ax: x_sub[i],
            ay: y_sub[i],
            xref: 'x',
            yref: 'y',
            axref: 'x',
            ayref: 'y',
            showarrow: true,
            arrowhead: 2,
            arrowsize: 1,
            arrowwidth: 1.5,
            arrowcolor: '#4F46E5'
        });
    }

    const layout = {
        title: `Campo Vectorial del Gradiente: ∇f = (∂f/∂x, ∂f/∂y)`,
        xaxis: { title: 'x' },
        yaxis: { title: 'y', scaleanchor: 'x' },
        annotations: annotations,
        height: 600,
        showlegend: false
    };

    Plotly.newPlot(containerId, traces, layout, { responsive: true });
}

function initializeVisualizations() {
    examples.forEach((example) => {
        createContourPlots(example, `contour-plot-${example.id}`);
        createSurfacePlots(example, `surface-plot-${example.id}`);
        createVectorPlot(example, `vector-plot-${example.id}`);
    });
}

function init() {
    initializeTabs();
    initializeVisualizations();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
