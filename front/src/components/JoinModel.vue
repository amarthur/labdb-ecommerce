<template>
    <div class="join-modal" v-if="isJoinModalShown">
      <div class="join-modal-content">
        <h2>Join</h2>
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="email">
        <label for="name">Name:</label>
        <input id="name" type="text" v-model="name">
        <label for="institute">Institute:</label>
        <input id="institute" type="text" v-model="institute">
        <button @click="handleJoin">Submit</button>
        <button @click="isJoinModalShown = false">Close</button>
        <p v-if="submitSuccess">Thank you for your submission. It has been sent for approval. You will be able to log in once your request is approved by our administrators.</p>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        isJoinModalShown: false,
        submitSuccess: false,
        email: '',
        name: '',
        institute: ''
      };
    },
    methods: {
      showJoinModal() {
        this.isJoinModalShown = true;
        this.submitSuccess = false;
      },
      handleJoin() {
        this.submitSuccess = true;
      }
    }
  }
  </script>

<style scoped>
.join-modal {
  display: flex;
  position: fixed;
  justify-content: center;
  align-items: center;
  z-index: 10;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.5);
}

.join-modal-content {
  display: flex;
  flex-direction: column;
  padding: 20px;
  width: 300px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.join-modal-content input {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.join-modal-content button {
  margin-top: 10px;
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

.join-modal-content button:hover {
  background-color: #0056b3;
}
</style>
