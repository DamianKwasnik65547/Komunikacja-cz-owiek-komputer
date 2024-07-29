document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const resultsContainer = document.querySelector('.results');
    
    if (form) {
        form.addEventListener('input', function() {
            calculateResults();
        });
    }

    function calculateResults() {
        const surfaceArea = parseFloat(document.getElementById('surface_area').value);
        const tileLength = parseFloat(document.getElementById('tile_length').value);
        const tileWidth = parseFloat(document.getElementById('tile_width').value);
        const sublayerThickness = parseFloat(document.getElementById('sublayer_thickness').value);
        const baseThickness = parseFloat(document.getElementById('base_thickness').value);
        const sandLayerThickness = parseFloat(document.getElementById('sand_layer_thickness').value);
        const excavationDepth = parseFloat(document.getElementById('excavation_depth').value);
        const jointWidth = parseFloat(document.getElementById('joint_width').value);
        const jointDepth = parseFloat(document.getElementById('joint_depth').value);
        const borderLength = parseFloat(document.getElementById('border_length').value);
        const borderSubs = parseFloat(document.getElementById('border_subs').value);
        const borderEarth = parseFloat(document.getElementById('border_earth').value);

        if (isNaN(surfaceArea) || isNaN(tileLength) || isNaN(tileWidth) || 
            isNaN(sublayerThickness) || isNaN(baseThickness) || 
            isNaN(sandLayerThickness) || isNaN(excavationDepth) || 
            isNaN(jointWidth) || isNaN(jointDepth) || isNaN(borderLength) || 
            isNaN(borderSubs) || isNaN(borderEarth)) {
            return;
        }

        const tiles = (surfaceArea * 10000) / (tileLength * tileWidth);
        const fugue = (surfaceArea * jointWidth * jointDepth) / 1000;
        const sublayer = (surfaceArea * sublayerThickness) / 1000;
        const base = (surfaceArea * baseThickness) / 1000;
        const sand = (surfaceArea * sandLayerThickness) / 1000;
        const excavation = (surfaceArea * excavationDepth) / 1000;

        // Display results
        resultsContainer.innerHTML = `
            <h2>Wyniki Obliczeń</h2>
            <ul>
                <li><strong>Ilość materiału nawierzchniowego:</strong> ${surfaceArea.toFixed(2)} m²</li>
                <li><strong>Ilość płytek:</strong> ${tiles.toFixed(2)}</li>
                <li><strong>Waga fugi:</strong> ${fugue.toFixed(2)} kg</li>
                <li><strong>Waga podsypki:</strong> ${sublayer.toFixed(2)} m³</li>
                <li><strong>Objętość podbudowy:</strong> ${base.toFixed(2)} m³</li>
                <li><strong>Waga piasku:</strong> ${sand.toFixed(2)} m³</li>
                <li><strong>Objętość wykopu:</strong> ${excavation.toFixed(2)} m³</li>
            </ul>
        `;
    }
});
