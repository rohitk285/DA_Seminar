document.getElementById('runBtn').addEventListener('click', async () => {
  const adj = document.getElementById('adjInput').value;
  const algo = document.getElementById('algo').value;
  const resEl = document.getElementById('result');
  resEl.textContent = 'Computing...';

  try {
    const resp = await fetch('/api/compute', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({adjacency: adj, algorithm: algo})
    });
    const data = await resp.json();
    if (data.error) {
      resEl.textContent = 'Error: ' + data.error;
      return;
    }

    // human-friendly result rendering
    function mkTable(rows, headers) {
      let html = '<div class="table-responsive"><table class="table table-sm table-striped">';
      html += '<thead><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr></thead>';
      html += '<tbody>' + rows.map(r => '<tr>' + r.map(c => `<td>${c}</td>`).join('') + '</tr>').join('') + '</tbody>';
      html += '</table></div>';
      return html;
    }

    let outHtml = '';
    const metric = data.metric || {};

    if (algo === 'betweenness' && metric.betweenness) {
      const entries = Object.entries(metric.betweenness).map(([k,v]) => [k, Number(v).toFixed(4)]);
      entries.sort((a,b) => Number(b[1]) - Number(a[1]));
      outHtml += '<h6>Betweenness Centrality (top nodes)</h6>';
      outHtml += mkTable(entries.slice(0, 50), ['Node','Betweenness']);
    } else if (algo === 'closeness' && metric.closeness) {
      const entries = Object.entries(metric.closeness).map(([k,v]) => [k, Number(v).toFixed(4)]);
      entries.sort((a,b) => Number(b[1]) - Number(a[1]));
      outHtml += '<h6>Closeness Centrality (top nodes)</h6>';
      outHtml += mkTable(entries.slice(0,50), ['Node','Closeness']);
    } else if (algo === 'jaccard' && metric.jaccard_pairs) {
      const rows = metric.jaccard_pairs.map(p => [String(p.pair), Number(p.jaccard).toFixed(4)]);
      rows.sort((a,b) => Number(b[1]) - Number(a[1]));
      outHtml += '<h6>Jaccard Coefficient (candidate links)</h6>';
      outHtml += mkTable(rows.slice(0,50), ['Node Pair','Jaccard']);
    } else if (algo === 'preferential' && metric.preferential_pairs) {
      const rows = metric.preferential_pairs.map(p => [String(p.pair), p.pac || p.pac === 0 ? p.pac : '']);
      rows.sort((a,b) => Number(b[1]) - Number(a[1]));
      outHtml += '<h6>Preferential Attachment (candidate links)</h6>';
      outHtml += mkTable(rows.slice(0,50), ['Node Pair','Score']);
    } else if (algo === 'girvan' && metric.communities) {
      outHtml += '<h6>Detected Communities</h6><ul>';
      metric.communities.forEach((c, i) => { outHtml += `<li><strong>Community ${i+1}:</strong> ${c.join(', ')}</li>`; });
      outHtml += '</ul>';
    } else {
      outHtml = '<pre>' + JSON.stringify(metric, null, 2) + '</pre>';
    }

    resEl.innerHTML = outHtml;

    // draw graph with Plotly (unchanged)
    const nodes = data.nodes;
    const edges = data.edges;

    const nodeX = nodes.map(n => n.x);
    const nodeY = nodes.map(n => n.y);
    const labels = nodes.map(n => n.id);

    const edgeX = [];
    const edgeY = [];
    edges.forEach(e => {
      const sIdx = labels.indexOf(e.source);
      const tIdx = labels.indexOf(e.target);
      if (sIdx >= 0 && tIdx >= 0) {
        edgeX.push(nodeX[sIdx], nodeX[tIdx], null);
        edgeY.push(nodeY[sIdx], nodeY[tIdx], null);
      }
    });

    const edgeTrace = {
      x: edgeX, y: edgeY, mode: 'lines', line: {color: '#888'}, hoverinfo: 'none', showlegend: false
    };

    const nodeTrace = {
      x: nodeX, y: nodeY, mode: 'markers+text', text: labels,
      textposition: 'top center', marker: {size: 18, color: '#1f77b4'}, hoverinfo: 'text'
    };

    const layout = {margin: {l:0,r:0,t:0,b:0}, xaxis: {visible:false}, yaxis:{visible:false}, height:420};

    Plotly.newPlot('graph', [edgeTrace, nodeTrace], layout, {responsive: true});
  } catch (err) {
    document.getElementById('result').textContent = String(err);
  }
});
