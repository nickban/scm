function updateStatus(orderId, field) {
  // Get the updated value from the input field
  var updatedValue = document.getElementById(field + '_' + orderId).value;
  console.log('updatedValue', updatedValue)
      // If the value is an empty string, set it to null
  if (updatedValue === '') {
        updatedValue = null;
    }

  // Prepare the data to send in the AJAX request
  var data = {
      order_id: orderId,
      field: field,
      value: updatedValue,
      csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value  // CSRF token for Django security
  };

  // Send an AJAX POST request to update the status field
  fetch('/order/update-status/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': data.csrfmiddlewaretoken  // Add CSRF token to the headers
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        showCustomAlert('更新成功!');
      } else {
        showCustomAlert('系统错误，请检查输入格式或网络情况!');
      }
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}


function showCustomAlert(message) {
  // Set the alert message
  document.getElementById('custom-alert-message').innerText = message;

  // Show the alert box
  document.getElementById('custom-alert').classList.remove('hidden');
}

function closeCustomAlert() {
  // Hide the alert box
  document.getElementById('custom-alert').classList.add('hidden');
}