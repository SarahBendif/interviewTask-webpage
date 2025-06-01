fetch('https://SarahBendif.github.io/interviewTask-webpage/patient_data.json')
  .then(response => response.json())
  .then(data => {
    console.log("🔥 Loaded Patient Data:", data);

    // === LINE CHART: Average Heart Rate ===
    const labels = data.map(d => d.date);
    const avgHeartRates = data.map(d =>
      d.vitals?.heart_rate?.reduce((a, b) => a + b, 0) / d.vitals?.heart_rate?.length || 0
    );

    new Chart(document.getElementById("lineChart"), {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: "Average Heart Rate",
          data: avgHeartRates,
          borderColor: 'red',
          fill: false
        }]
      }
    });

    // === BAR CHART: Steps vs. Calories ===
    const steps = data.map(d => d.activity?.steps || 0);
    const calories = data.map(d => d.nutrition?.calories || 0);

    new Chart(document.getElementById("barChart"), {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Steps",
            data: steps,
            backgroundColor: "blue"
          },
          {
            label: "Calories",
            data: calories,
            backgroundColor: "orange"
          }
        ]
      }
    });

    // === DONUT CHART: Sleep Quality Distribution ===
    const qualityCounts = data.reduce((acc, d) => {
      const q = d.sleep?.quality || "unknown";
      acc[q] = (acc[q] || 0) + 1;
      return acc;
    }, {});

    new Chart(document.getElementById("donutChart"), {
      type: "doughnut",
      data: {
        labels: Object.keys(qualityCounts),
        datasets: [{
          data: Object.values(qualityCounts),
          backgroundColor: ["green", "yellow", "red", "purple"]
        }]
      }
    });
  })
  .catch(err => {
    console.error("Error loading patient_data.json", err);
  });
