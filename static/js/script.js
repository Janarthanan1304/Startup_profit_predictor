const predictBtn = document.getElementById('predict-btn');
const predictedProfitElement = document.getElementById('predicted-profit');

predictBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  const rdSpend = parseFloat(document.getElementById('R&D-Spend').value);
  const administration = parseFloat(document.getElementById('Administration').value);
  const marketingSpend = parseFloat(document.getElementById('Marketing-Spend').value);
  const state = document.getElementById('state').value;

  const formData = new FormData();
  formData.append('R&D Spend', rdSpend);
  formData.append('Administration', administration);
  formData.append('Marketing Spend', marketingSpend);
  formData.append('state', state);

  try {
    console.log('Sending request to /predict endpoint...');
    const response = await axios.post('/predict', formData);
    console.log('Response received from /predict endpoint...');
    console.log(response.data);

    if (response.data.predicted_profit) {
      const predictedProfit = response.data.predicted_profit;
      console.log('Predicted profit:', predictedProfit);
      predictedProfitElement.innerText = `Predicted Profit: $${predictedProfit}`;
    } else {
      console.error('Error: No predicted profit found in response data.');
    }
  } catch (error) {
    console.error('Error:', error);
  }
});
