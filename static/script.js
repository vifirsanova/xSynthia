document.addEventListener('DOMContentLoaded', function() {
    // Setup event listeners
    document.getElementById('startingPoint').addEventListener('change', updateStartingPointInputs);
    document.getElementById('visualizationLevels').addEventListener('change', showLevelInfo);
    document.getElementById('graphType').addEventListener('change', showGraphTypeInfo);
    document.getElementById('generateBtn').addEventListener('click', generateGraph);
});

function updateStartingPointInputs() {
    const startingPoint = document.getElementById('startingPoint').value;
    document.getElementById('defaultInput').classList.add('hidden');
    document.getElementById('randomSeedInput').classList.add('hidden');
    document.getElementById('setWordInput').classList.add('hidden');

    if (startingPoint === 'default') {
        document.getElementById('defaultInput').classList.remove('hidden');
    } else if (startingPoint === 'randomSeed') {
        document.getElementById('randomSeedInput').classList.remove('hidden');
    } else if (startingPoint === 'setWord') {
        document.getElementById('setWordInput').classList.remove('hidden');
    }
}

function showLevelInfo() {
    const levelInfo = document.getElementById('levelInfo');
    const selectedLevel = document.getElementById('visualizationLevels').value;

    const infoText = {
        associationNetwork: "associations, visualized in a basic network",
        semanticRelations: "includes synonyms, antonyms, hyponyms, hypernyms, meronyms, holonyms, and co-occurrence patterns"
    };

    levelInfo.textContent = infoText[selectedLevel] || "";
    levelInfo.classList.remove('hidden');
}

function showGraphTypeInfo() {
    const graphTypeInfo = document.getElementById('graphTypeInfo');
    const selectedGraphType = document.getElementById('graphType').value;

    const graphInfoText = {
        weightedGraph: "Show me subgraphs: A weighted graph to represent the strength of associations and extract subgraphs by filtering edges based on weight thresholds",
        multilayerGraph: "Show layers of associations: A multilayer graph or hierarchical graph to organize associations into different levels or domains"
    };

    graphTypeInfo.textContent = graphInfoText[selectedGraphType] || "";
    graphTypeInfo.classList.remove('hidden');
}

function generateGraph() {
    const model = document.getElementById('model').value;
    const startingPoint = document.getElementById('startingPoint').value;
    const visualizationLevels = document.getElementById('visualizationLevels').value;

    let startingDetails = null;
    if (startingPoint === 'randomSeed') {
        startingDetails = document.getElementById('randomSeedValue').value;
    } else if (startingPoint === 'setWord') {
        startingDetails = document.getElementById('wordList').value;
    }

    // Replace graph placeholder content
    const placeholder = document.querySelector('.graph-placeholder');
    placeholder.innerHTML = '<p>Please, wait...<br>The graph is being generated based on the selected settings</p>';
    
    setTimeout(() => {
        placeholder.innerHTML = '<iframe src="jailbreaking_ios.html" style="width: 100%; height: 100%; border: none;"></iframe>';
    }, 3000);

    // Save settings
    const formData = new FormData(document.getElementById('settingsForm'));

    fetch('/save-settings', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Settings saved:', data);
    })
    .catch(error => {
        console.error('Error saving settings:', error);
    });
}