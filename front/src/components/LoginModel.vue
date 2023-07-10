<template>
    <div class="login-model" v-if="isLoginModelShown">
      <div class="login-model-content">
        <h2>Login</h2>
        <label for="username">Username:</label>
        <input id="username" type="text">
        <label for="password">Password:</label>
        <input id="password" type="password">
        <button @click="handleLogin">Submit</button>
        <button @click="isLoginModelShown = false">Close</button>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        isLoginModelShown: false,
      };
    },
    methods: {
      showLoginModel() {
        this.isLoginModelShown = true;
      },
      handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:5000/api/authenticate', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
            username: username,
            password: password
            })
        })
        .then(response => {
            if (response.ok) {
                this.$emit('login-success');
                this.isLoginModelShown = false;
                return response.json();
            } else {
                throw new Error('Invalid credentials');
            }
        })
        .then(data => {
            console.log(data.message);
            this.isLoginModelShown = false; // Close the model when login is successful
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

    }
  }
  </script>

  <style scoped>
  .login-model {
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.4);
  }

  .login-model-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    border-radius: 15px;
  }

  .login-model-content h2 {
    margin-top: 0;
  }

  .login-model-content label {
    display: block;
    margin: 0.5em 0;
  }

  .login-model-content input {
    width: 100%;
    padding: 0.5em;
    margin-bottom: 1em;
  }

  .login-model-content button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
    border-radius: 4px;
  }

  .login-model-content button:hover {
    opacity: 0.8;
  }
  </style>

