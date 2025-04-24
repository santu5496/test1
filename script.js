function handleSubmit() {
  fetch('/run_python_function', { method: 'POST' })
    .then(response => {
      if (response.ok) {
        console.log('Python function called successfully');
      } else {
        console.error('Error calling Python function');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}